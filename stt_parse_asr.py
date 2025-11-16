import json
from typing import List, Dict, Any

def parse_asr_messages_to_dialogue(json_messages: List[str]) -> str:
    """
    Парсит поток JSON сообщений от ASR системы и формирует диалог.
    
    Args:
        json_messages: Список JSON строк от ASR системы
        
    Returns:
        Строка с отформатированным диалогом
    """
    
    # Словарь для хранения текущих реплик по каналам
    current_utterances = {}
    # Список завершенных реплик
    completed_utterances = []
    
    for msg_str in json_messages:
        try:
            message = json.loads(msg_str)
            result = message.get('result', {})
            channel_tag = result.get('channelTag', '0')
            
            # Обрабатываем финальное уточненное сообщение (самый качественный текст)
            if 'finalRefinement' in result:
                refinement = result['finalRefinement']
                normalized_text = refinement.get('normalizedText', {})
                
                if normalized_text and 'alternatives' in normalized_text:
                    alt = normalized_text['alternatives'][0]
                    text = alt.get('text', '').strip()
                    start_time = alt.get('startTimeMs', 0)
                    end_time = alt.get('endTimeMs', 0)
                    final_index = refinement.get('finalIndex', 0)
                    
                    if text:
                        # Сохраняем/обновляем текущую реплику
                        current_utterances[channel_tag] = {
                            'text': text,
                            'start_time': int(start_time),
                            'end_time': int(end_time),
                            'channel': channel_tag,
                            'final_index': final_index
                        }
            
            # Обрабатываем сообщение о конце высказывания
            elif 'eouUpdate' in result:
                eou_time = result['eouUpdate'].get('timeMs', 0)
                channel_tag = result.get('channelTag', '0')
                
                # Если есть текущая реплика для этого канала, завершаем ее
                if channel_tag in current_utterances:
                    utterance = current_utterances[channel_tag]
                    
                    # Обновляем время окончания на время из EOU, если оно больше
                    if int(eou_time) > utterance['end_time']:
                        utterance['end_time'] = int(eou_time)
                    
                    # Добавляем в список завершенных реплик
                    completed_utterances.append(utterance.copy())
                    
                    # Очищаем текущую реплику для этого канала
                    del current_utterances[channel_tag]
                    
        except json.JSONDecodeError:
            continue  # Пропускаем некорректные JSON
        except (TypeError, ValueError) as e:
            print(f"Ошибка преобразования данных: {e}")
            continue
    
    # Добавляем оставшиеся незавершенные реплики (на случай если EOU не пришло)
    for utterance in current_utterances.values():
        completed_utterances.append(utterance)
    
    # Сортируем реплики по времени начала
    completed_utterances.sort(key=lambda x: x['start_time'])
    
    # Форматируем результат
    return format_dialogue(completed_utterances)

def format_dialogue(utterances: List[Dict]) -> str:
    """
    Форматирует список реплик в читаемый диалог.
    
    Args:
        utterances: Список реплик
        
    Returns:
        Отформатированная строка с диалогом
    """
    lines = []
    
    for i, utt in enumerate(utterances, 1):
        speaker = f"Спикер {int(utt['channel']) + 1}"
        text = utt['text']
        start_sec = utt['start_time'] / 1000.0
        end_sec = utt['end_time'] / 1000.0
        
        line = f"{i}. [{speaker}] {start_sec:.2f}-{end_sec:.2f}с: {text}"
        lines.append(line)
    
    return "\n".join(lines)

def format_dialogue_from_asr(json_messages: List[str]) -> str:
    """
    Основная функция для использования извне.
    Просто вызывает parse_asr_messages_to_dialogue с проверкой ошибок.
    """
    try:
        return parse_asr_messages_to_dialogue(json_messages)
    except Exception as e:
        return f"Ошибка при форматировании диалога: {e}"
import { useState } from 'react';
import { Pressable, Text, View } from 'react-native';

export default function QuestionCard(props) {
  const item = props.item;
  const [selectedChoiceId, setSelectedChoiceId] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const selectedChoice = item.choices.find((choice) => choice.id === selectedChoiceId);

  return (
    <View>
      <Text>{item.label}</Text>
      <Text>{item.prompt}</Text>
      {item.choices.map((choice) => (
        <Pressable key={choice.id} disabled={submitted} onPress={() => setSelectedChoiceId(choice.id)}>
          <Text>{selectedChoiceId === choice.id ? '✓ ' : ''}{choice.text}</Text>
        </Pressable>
      ))}
      <Pressable disabled={!selectedChoiceId || submitted} onPress={() => setSubmitted(true)}>
        <Text>Submit internal fixture answer</Text>
      </Pressable>
      {submitted ? (
        <View>
          <Text>Selected: {selectedChoice?.text}</Text>
          <Text>{item.feedback}</Text>
          <Text>No outcome calculation, persistence, telemetry, or remote call was produced.</Text>
        </View>
      ) : (
        <Text>Feedback is hidden until submit.</Text>
      )}
    </View>
  );
}

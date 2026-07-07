import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function QuestionCard(props) {
  const item = props.item;
  const [selectedChoiceId, setSelectedChoiceId] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const selectedChoice = item.choices.find((choice) => choice.id === selectedChoiceId);

  function resetLocalSelection() {
    setSelectedChoiceId(null);
    setSubmitted(false);
  }

  return (
    <View style={styles.card}>
      <Text style={styles.kicker}>{item.label}</Text>
      <Text style={styles.track}>{item.track}</Text>
      <Text style={styles.prompt}>{item.prompt}</Text>

      {item.choices.map((choice) => {
        const selected = selectedChoiceId === choice.id;
        return (
          <Pressable
            key={choice.id}
            disabled={submitted}
            onPress={() => setSelectedChoiceId(choice.id)}
            style={({ pressed }) => [
              styles.choice,
              selected && styles.selectedChoice,
              submitted && styles.disabledChoice,
              pressed && !submitted && styles.pressedChoice
            ]}
          >
            <Text style={[styles.choiceText, selected && styles.selectedChoiceText]}>
              {selected ? '✓ ' : ''}{choice.text}
            </Text>
          </Pressable>
        );
      })}

      <Pressable
        disabled={!selectedChoiceId || submitted}
        onPress={() => setSubmitted(true)}
        style={[styles.submitButton, (!selectedChoiceId || submitted) && styles.submitButtonDisabled]}
      >
        <Text style={styles.submitText}>Submit internal fixture answer</Text>
      </Pressable>

      {submitted ? (
        <View style={styles.feedbackBox}>
          <Text style={styles.feedbackTitle}>Feedback unlocked after submit</Text>
          <Text style={styles.feedbackBody}>Selected: {selectedChoice?.text}</Text>
          <Text style={styles.feedbackBody}>{item.feedback}</Text>
          <Text style={styles.noOutcome}>No outcome calculation, persistence, telemetry, or remote call was produced.</Text>
          <Pressable onPress={resetLocalSelection} style={styles.resetButton}>
            <Text style={styles.resetText}>Reset local fixture interaction</Text>
          </Pressable>
        </View>
      ) : (
        <Text style={styles.helperText}>Choose one local fixture answer. Feedback remains hidden until submit.</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderColor: '#1f2937',
    backgroundColor: '#ffffff',
    borderRadius: 18,
    padding: 16,
    marginBottom: 16
  },
  kicker: {
    color: '#6b7280',
    fontSize: 12,
    fontWeight: '800',
    textTransform: 'uppercase',
    marginBottom: 4
  },
  track: {
    color: '#1d4ed8',
    fontSize: 13,
    fontWeight: '900',
    marginBottom: 8
  },
  prompt: {
    color: '#111827',
    fontSize: 18,
    fontWeight: '800',
    lineHeight: 25,
    marginBottom: 14
  },
  choice: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    backgroundColor: '#f9fafb',
    borderRadius: 14,
    padding: 14,
    marginBottom: 10
  },
  selectedChoice: {
    borderColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  disabledChoice: {
    opacity: 0.75
  },
  pressedChoice: {
    borderColor: '#2563eb'
  },
  choiceText: {
    color: '#374151',
    fontSize: 15,
    lineHeight: 21
  },
  selectedChoiceText: {
    color: '#1e3a8a',
    fontWeight: '800'
  },
  submitButton: {
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 14,
    alignItems: 'center',
    marginTop: 4
  },
  submitButtonDisabled: {
    backgroundColor: '#9ca3af'
  },
  submitText: {
    color: '#ffffff',
    fontWeight: '900',
    fontSize: 14
  },
  helperText: {
    color: '#6b7280',
    fontSize: 13,
    lineHeight: 19,
    marginTop: 10
  },
  feedbackBox: {
    borderWidth: 1,
    borderColor: '#166534',
    backgroundColor: '#f0fdf4',
    borderRadius: 14,
    padding: 14,
    marginTop: 12
  },
  feedbackTitle: {
    color: '#166534',
    fontSize: 14,
    fontWeight: '900',
    marginBottom: 8
  },
  feedbackBody: {
    color: '#14532d',
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 6
  },
  noOutcome: {
    color: '#7f1d1d',
    fontSize: 13,
    fontWeight: '800',
    lineHeight: 19,
    marginTop: 4
  },
  resetButton: {
    borderWidth: 1,
    borderColor: '#166534',
    borderRadius: 12,
    padding: 12,
    alignItems: 'center',
    marginTop: 12
  },
  resetText: {
    color: '#166534',
    fontSize: 13,
    fontWeight: '900'
  }
});

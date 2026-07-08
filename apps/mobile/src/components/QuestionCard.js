import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function QuestionCard(props) {
  const item = props.item;
  const [selectedChoiceId, setSelectedChoiceId] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const selectedChoice = item.choices.find((choice) => choice.id === selectedChoiceId);

  function resetLocalFixture() {
    setSelectedChoiceId(null);
    setSubmitted(false);
  }

  return (
    <View style={styles.card}>
      <Text style={styles.sectionLabel}>Internal fixture interaction</Text>
      <Text style={styles.track}>{item.track}</Text>
      <Text style={styles.label}>{item.label}</Text>
      <Text style={styles.prompt}>{item.prompt}</Text>

      <View style={styles.choiceGroup}>
        {item.choices.map((choice) => {
          const selected = selectedChoiceId === choice.id;
          return (
            <Pressable
              key={choice.id}
              disabled={submitted}
              onPress={() => setSelectedChoiceId(choice.id)}
              style={({ pressed }) => [
                styles.choice,
                selected && styles.choiceSelected,
                submitted && styles.choiceLocked,
                pressed && !submitted && styles.choicePressed
              ]}
            >
              <Text style={[styles.choiceText, selected && styles.choiceTextSelected]}>
                {selected ? '✓ Selected — ' : ''}{choice.text}
              </Text>
            </Pressable>
          );
        })}
      </View>

      <Pressable
        disabled={!selectedChoiceId || submitted}
        onPress={() => setSubmitted(true)}
        style={[styles.submitButton, (!selectedChoiceId || submitted) && styles.submitButtonDisabled]}
      >
        <Text style={styles.submitText}>{submitted ? 'Submitted locally' : 'Submit internal fixture answer'}</Text>
      </Pressable>

      {submitted ? (
        <View style={styles.feedbackBox}>
          <Text style={styles.feedbackTitle}>Feedback-after-submit</Text>
          <Text style={styles.feedbackText}>Selected: {selectedChoice?.text}</Text>
          <Text style={styles.feedbackText}>{item.feedback}</Text>
          <Text style={styles.noOutcome}>No score, readiness, pass/fail, persistence, telemetry, or remote call was produced.</Text>
          <Pressable onPress={resetLocalFixture} style={styles.resetButton}>
            <Text style={styles.resetText}>Reset local fixture interaction</Text>
          </Pressable>
        </View>
      ) : (
        <Text style={styles.helperText}>Select one local fixture answer. Feedback appears only after submit.</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderColor: '#1f2937',
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 16,
    marginBottom: 18
  },
  sectionLabel: {
    color: '#6b7280',
    fontSize: 12,
    fontWeight: '900',
    letterSpacing: 1,
    marginBottom: 4,
    textTransform: 'uppercase'
  },
  track: {
    color: '#1d4ed8',
    fontSize: 13,
    fontWeight: '900',
    marginBottom: 6
  },
  label: {
    color: '#4b5563',
    fontSize: 13,
    fontWeight: '800',
    marginBottom: 8
  },
  prompt: {
    color: '#111827',
    fontSize: 18,
    fontWeight: '900',
    lineHeight: 26,
    marginBottom: 14
  },
  choiceGroup: {
    marginBottom: 6
  },
  choice: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    backgroundColor: '#f9fafb',
    borderRadius: 15,
    padding: 14,
    marginBottom: 10
  },
  choiceSelected: {
    borderColor: '#1d4ed8',
    backgroundColor: '#dbeafe'
  },
  choiceLocked: {
    opacity: 0.82
  },
  choicePressed: {
    borderColor: '#2563eb'
  },
  choiceText: {
    color: '#374151',
    fontSize: 15,
    lineHeight: 21
  },
  choiceTextSelected: {
    color: '#1e3a8a',
    fontWeight: '900'
  },
  submitButton: {
    alignItems: 'center',
    backgroundColor: '#111827',
    borderRadius: 15,
    padding: 14,
    marginTop: 2
  },
  submitButtonDisabled: {
    backgroundColor: '#9ca3af'
  },
  submitText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '900'
  },
  helperText: {
    color: '#6b7280',
    fontSize: 13,
    lineHeight: 19,
    marginTop: 10
  },
  feedbackBox: {
    borderWidth: 1,
    borderColor: '#15803d',
    backgroundColor: '#f0fdf4',
    borderRadius: 15,
    padding: 14,
    marginTop: 12
  },
  feedbackTitle: {
    color: '#166534',
    fontSize: 14,
    fontWeight: '900',
    marginBottom: 8
  },
  feedbackText: {
    color: '#14532d',
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 6
  },
  noOutcome: {
    color: '#7f1d1d',
    fontSize: 13,
    fontWeight: '900',
    lineHeight: 19,
    marginTop: 4
  },
  resetButton: {
    borderWidth: 1,
    borderColor: '#166534',
    borderRadius: 13,
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

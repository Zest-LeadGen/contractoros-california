import { StyleSheet, Text, View } from 'react-native';

export default function InternalBanner() {
  return (
    <View style={styles.container}>
      <Text style={styles.eyebrow}>INTERNAL-ONLY</Text>
      <Text style={styles.title}>ContractorOS California</Text>
      <View style={styles.warningGrid}>
        <Text style={styles.warningPill}>FIXTURE-ONLY</Text>
        <Text style={styles.warningPill}>NOT PUBLIC</Text>
        <Text style={styles.warningPill}>NOT EXAM-READY</Text>
      </View>
      <Text style={styles.noOutcome}>NO SCORE / NO READINESS / NO PASS-FAIL</Text>
      <Text style={styles.body}>
        Controlled mobile scaffold for internal QA only. Content is local fixture data and must not be treated as production, public exam, or learner readiness material.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderWidth: 2,
    borderColor: '#92400e',
    backgroundColor: '#fff7ed',
    borderRadius: 18,
    padding: 18,
    marginBottom: 18
  },
  eyebrow: {
    fontSize: 13,
    fontWeight: '900',
    letterSpacing: 1.4,
    color: '#9a3412',
    marginBottom: 8
  },
  title: {
    fontSize: 28,
    fontWeight: '900',
    color: '#111827',
    marginBottom: 12
  },
  warningGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 10
  },
  warningPill: {
    borderWidth: 1,
    borderColor: '#c2410c',
    backgroundColor: '#ffedd5',
    color: '#7c2d12',
    fontSize: 12,
    fontWeight: '900',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    marginRight: 8,
    marginBottom: 8
  },
  noOutcome: {
    color: '#7f1d1d',
    fontSize: 14,
    fontWeight: '900',
    marginBottom: 10
  },
  body: {
    color: '#374151',
    fontSize: 14,
    lineHeight: 21
  }
});

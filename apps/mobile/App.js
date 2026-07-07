import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import InternalBanner from './src/components/InternalBanner';
import QuestionCard from './src/components/QuestionCard';
import TrackStatusCard from './src/components/TrackStatusCard';
import { internalQuestion, trackStatuses } from './src/data/internalFixtureItems';

const blockedScopeItems = [
  'No score calculation',
  'No readiness result',
  'No pass/fail result',
  'No backend',
  'No saved progress',
  'No auth, login, or user accounts',
  'No payments or subscriptions',
  'No analytics',
  'No Question Bank migration',
  'No public MCQs',
  'No C10 public content'
];

export default function App() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.content}>
        <InternalBanner />

        <View style={styles.section}>
          <Text style={styles.sectionLabel}>Track status</Text>
          <Text style={styles.sectionTitle}>Internal fixture tracks</Text>
          {trackStatuses.map((track) => (
            <TrackStatusCard
              key={track.id}
              title={track.title}
              status={track.status}
              description={track.description}
            />
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionLabel}>Internal fixture interaction</Text>
          <Text style={styles.sectionTitle}>Local-only question flow</Text>
          <QuestionCard item={internalQuestion} />
        </View>

        <View style={styles.blockedSection}>
          <Text style={styles.sectionLabel}>Blocked scope text</Text>
          <Text style={styles.sectionTitle}>Not implemented in this scaffold</Text>
          {blockedScopeItems.map((item) => (
            <Text key={item} style={styles.blockedItem}>• {item}</Text>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f3f4f6'
  },
  content: {
    padding: 20,
    paddingBottom: 36
  },
  section: {
    marginBottom: 20
  },
  blockedSection: {
    borderWidth: 1,
    borderColor: '#6b7280',
    backgroundColor: '#ffffff',
    borderRadius: 18,
    padding: 16,
    marginBottom: 20
  },
  sectionLabel: {
    color: '#6b7280',
    fontSize: 12,
    fontWeight: '900',
    letterSpacing: 1,
    textTransform: 'uppercase',
    marginBottom: 4
  },
  sectionTitle: {
    color: '#111827',
    fontSize: 21,
    fontWeight: '900',
    marginBottom: 12
  },
  blockedItem: {
    color: '#374151',
    fontSize: 14,
    lineHeight: 22,
    marginBottom: 4
  }
});

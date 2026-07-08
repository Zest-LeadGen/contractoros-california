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
          <Text style={styles.sectionTitle}>Phase One internal tracks</Text>
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
          <QuestionCard item={internalQuestion} />
        </View>

        <View style={styles.blockedSection}>
          <Text style={styles.sectionLabel}>Blocked scope text</Text>
          <Text style={styles.sectionTitle}>Explicitly not included</Text>
          <Text style={styles.blockedIntro}>
            These items remain blocked in this internal scaffold unless a later approved gate changes scope.
          </Text>
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
    paddingBottom: 40
  },
  section: {
    marginBottom: 20
  },
  sectionLabel: {
    color: '#6b7280',
    fontSize: 12,
    fontWeight: '900',
    letterSpacing: 1,
    marginBottom: 4,
    textTransform: 'uppercase'
  },
  sectionTitle: {
    color: '#111827',
    fontSize: 22,
    fontWeight: '900',
    lineHeight: 28,
    marginBottom: 12
  },
  blockedSection: {
    borderWidth: 1,
    borderColor: '#6b7280',
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 16,
    marginBottom: 20
  },
  blockedIntro: {
    color: '#4b5563',
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 10
  },
  blockedItem: {
    color: '#374151',
    fontSize: 14,
    lineHeight: 22,
    marginBottom: 4
  }
});

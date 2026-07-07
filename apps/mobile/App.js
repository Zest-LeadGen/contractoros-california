import { SafeAreaView, ScrollView, Text, View } from 'react-native';
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
    <SafeAreaView>
      <ScrollView>
        <InternalBanner />
        <View>
          <Text>Track status</Text>
          {trackStatuses.map((track) => (
            <TrackStatusCard
              key={track.id}
              title={track.title}
              status={track.status}
              description={track.description}
            />
          ))}
        </View>
        <View>
          <Text>Internal fixture interaction</Text>
          <QuestionCard item={internalQuestion} />
        </View>
        <View>
          <Text>Blocked scope</Text>
          {blockedScopeItems.map((item) => (
            <Text key={item}>• {item}</Text>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

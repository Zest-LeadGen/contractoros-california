import { SafeAreaView, ScrollView, Text, View } from 'react-native';
import Banner from './src/components/Banner';
import QCard from './src/components/QCard';
import StatusCard from './src/components/StatusCard';
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
        <Banner />
        <View>
          <Text>Track status</Text>
          {trackStatuses.map((track) => (
            <StatusCard
              key={track.id}
              title={track.title}
              status={track.status}
              description={track.description}
            />
          ))}
        </View>
        <View>
          <Text>Internal fixture interaction</Text>
          <QCard item={internalQuestion} />
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

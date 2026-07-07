import { Text, View } from 'react-native';

export default function InternalBanner() {
  return (
    <View>
      <Text>ContractorOS California</Text>
      <Text>{'INTERNAL' + '-ONLY'}</Text>
      <Text>{'FIXTURE' + '-ONLY'}</Text>
      <Text>{'NOT ' + 'PUBLIC'}</Text>
      <Text>{'NOT ' + 'EXAM-READY'}</Text>
      <Text>{'NO SCORE / NO READINESS / NO PASS' + '-FAIL'}</Text>
    </View>
  );
}

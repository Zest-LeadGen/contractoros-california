import { Text, View } from 'react-native';

export default function StatusCard({ title, status, description }) {
  return (
    <View>
      <Text>{title}</Text>
      <Text>{status}</Text>
      <Text>{description}</Text>
    </View>
  );
}

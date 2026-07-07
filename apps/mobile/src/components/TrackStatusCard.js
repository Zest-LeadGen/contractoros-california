import { Text, View } from 'react-native';

export default function TrackStatusCard(props) {
  return (
    <View>
      <Text>{props.title}</Text>
      <Text>{props.status}</Text>
      <Text>{props.description}</Text>
    </View>
  );
}

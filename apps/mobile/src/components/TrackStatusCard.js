import { StyleSheet, Text, View } from 'react-native';

export default function TrackStatusCard(props) {
  const isBlocked = props.status.toLowerCase().includes('blocked');

  return (
    <View style={[styles.card, isBlocked ? styles.blockedCard : styles.activeCard]}>
      <Text style={styles.title}>{props.title}</Text>
      <Text style={[styles.status, isBlocked ? styles.blockedStatus : styles.activeStatus]}>
        {props.status}
      </Text>
      <Text style={styles.description}>{props.description}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
    marginBottom: 12
  },
  activeCard: {
    borderColor: '#166534',
    backgroundColor: '#f0fdf4'
  },
  blockedCard: {
    borderColor: '#991b1b',
    backgroundColor: '#fef2f2'
  },
  title: {
    color: '#111827',
    fontSize: 18,
    fontWeight: '800',
    marginBottom: 6
  },
  status: {
    fontSize: 13,
    fontWeight: '900',
    marginBottom: 8,
    textTransform: 'uppercase'
  },
  activeStatus: {
    color: '#166534'
  },
  blockedStatus: {
    color: '#991b1b'
  },
  description: {
    color: '#374151',
    fontSize: 14,
    lineHeight: 20
  }
});

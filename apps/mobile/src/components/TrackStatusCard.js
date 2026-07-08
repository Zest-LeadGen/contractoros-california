import { StyleSheet, Text, View } from 'react-native';

export default function TrackStatusCard(props) {
  const isBlocked = props.status.toLowerCase().includes('blocked') || props.status.toLowerCase().includes('deferred');
  const statusLabel = isBlocked ? 'C10 deferred / blocked' : 'Law & Business active internal fixture track';

  return (
    <View style={[styles.card, isBlocked ? styles.blockedCard : styles.activeCard]}>
      <Text style={styles.title}>{props.title}</Text>
      <Text style={[styles.status, isBlocked ? styles.blockedStatus : styles.activeStatus]}>{statusLabel}</Text>
      <Text style={styles.description}>{props.description}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderRadius: 18,
    padding: 16,
    marginBottom: 12
  },
  activeCard: {
    borderColor: '#15803d',
    backgroundColor: '#f0fdf4'
  },
  blockedCard: {
    borderColor: '#b91c1c',
    backgroundColor: '#fef2f2'
  },
  title: {
    color: '#111827',
    fontSize: 18,
    fontWeight: '900',
    marginBottom: 6
  },
  status: {
    fontSize: 13,
    fontWeight: '900',
    letterSpacing: 0.4,
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

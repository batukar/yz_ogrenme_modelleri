import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, TouchableOpacity, Platform } from 'react-native';
import { Picker } from '@react-native-picker/picker';

export default function HomeScreen() {
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState<keyof typeof genderMap | ''>('');
  const [familyHistory, setFamilyHistory] = useState<keyof typeof familyHistoryMap | ''>('');
  const [workInterfere, setWorkInterfere] = useState('');
  const [careOptions, setCareOptions] = useState<keyof typeof binaryMap | ''>('');
  const [noEmployees, setNoEmployees] = useState('');
  const [benefits, setBenefits] = useState<keyof typeof binaryMap | ''>('');
  const [anonymity, setAnonymity] = useState<keyof typeof binaryMap | ''>('');
  const [coworkers, setCoworkers] = useState<keyof typeof coworkersMap | ''>('');
  const [supervisor, setSupervisor] = useState<keyof typeof supervisorMap | ''>('');
  const [result, setResult] = useState<{ prediction?: number; probability?: number; error?: string } | null>(null);
  const [error, setError] = useState('');

  const ageOptions = Array.from({ length: 50 }, (_, i) => (i + 16).toString());
  const employeeRanges = [
    { label: '1-5 Kişi', value: '1-5' },
    { label: '6-25 Kişi', value: '6-25' },
    { label: '26-100 Kişi', value: '26-100' },
    { label: '100-500 Kişi', value: '100-500' },
    { label: '500-1000 Kişi', value: '500-1000' },
    { label: '1000+ Kişi', value: 'More than 1000' }
  ];
  const binaryOptions = [
    { label: 'Evet', value: 'Yes' },
    { label: 'Hayır', value: 'No' }
  ];
  const workInterfereOptions = [
    { label: 'Asla', value: 'Never' },
    { label: 'Nadiren', value: 'Rarely' },
    { label: 'Bazen', value: 'Sometimes' },
    { label: 'Sıklıkla', value: 'Often' }
  ];
  const genderMap = { 'Erkek': 'Male', 'Kadın': 'Female' };
  const familyHistoryMap = { 'Var': 'Yes', 'Yok': 'No' };
  const binaryMap = { 'Evet': 'Yes', 'Hayır': 'No' };
  const coworkersMap = { 'Evet': 'Yes', 'Bazılarından': 'Some of them', 'Hayır': 'No'};
  const supervisorMap = { 'Evet': 'Yes', 'Hayır': 'No' };


  const validateEmail = (email: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };
  
  const validateInputs = () => {
    if (!email || !validateEmail(email)) {
      setError('Lütfen geçerli bir email adresi giriniz.');
      return false;
    }
  
    if (!age || !gender || !familyHistory || !workInterfere || !careOptions || !noEmployees || !benefits || !anonymity || !coworkers || !supervisor) {
      setError('Lütfen tüm alanları doldurun.');
      return false;
    }
  
    setError('');
    return true;
  };

  const handleSubmit = async () => {
    if (!validateInputs()) return;

    try {
      const response = await fetch('http://10.25.1.187:5001/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          Age: parseInt(age),
          Gender: gender ? genderMap[gender] : '',
          family_history: familyHistory ? familyHistoryMap[familyHistory] : '',
          work_interfere: workInterfere,
          care_options: careOptions ? binaryMap[careOptions] : '',
          no_employees: noEmployees,
          benefits: benefits ? binaryMap[benefits] : '',
          anonymity: anonymity ? binaryMap[anonymity] : '',
          coworkers: coworkers ? coworkersMap[coworkers] : '',
          supervisor: supervisor ? supervisorMap[supervisor] : '',
          tech_company: 'Yes',
          wellness_program: 'No'
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (e) {
      setResult({ error: 'Sunucuya bağlanılamadı.' });
    }
  };

  const RadioGroup: React.FC<{ label: string; options: string[]; selected: string; onSelect: (value: string) => void }> = ({ label, options, selected, onSelect }) => (
    <View style={styles.radioGroup}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.radioOptions}>
        {options.map(opt => (
          <TouchableOpacity key={opt} style={styles.radioButton} onPress={() => onSelect(opt)}>
            <View style={styles.radioCircle}>{selected === opt && <View style={styles.radioDot} />}</View>
            <Text>{opt}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  return (
    <ScrollView contentContainerStyle={[styles.container, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
      <Text style={styles.title}>🧠 Zihinsel Sağlık Tahmini</Text>
      <Text style={styles.label}>📧 Lütfen email adresinizi giriniz:</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        placeholderTextColor="#999"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />
      <Text style={styles.label}>🎂 Yaşınız (16-65 arası):</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={age}
          onValueChange={setAge}
          style={Platform.OS === 'ios' ? styles.pickerIOS : styles.pickerAndroid}
          mode="dropdown"
        >
          <Picker.Item label="Yaş Seçiniz" value="" color="#999" />
          {ageOptions.map(a => (
            <Picker.Item key={a} label={a} value={a} color="#000" />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>🚻 Cinsiyetiniz:</Text>
      <RadioGroup options={["Erkek", "Kadın"]} selected={gender} onSelect={(value) => setGender(value as keyof typeof genderMap)} label={''} />

      <Text style={styles.label}>🧬 Ailenizde zihinsel sağlık geçmişi var mı?</Text>
      <RadioGroup options={["Var", "Yok"]} selected={familyHistory} onSelect={(value) => setFamilyHistory(value as keyof typeof familyHistoryMap)} label={''} />

      <Text style={styles.label}>🏢 İş yerinizde zihinsel sağlık desteği sunuluyor mu?</Text>
      <RadioGroup options={binaryOptions.map(opt => opt.label)} selected={careOptions} onSelect={(value) => setCareOptions(value as keyof typeof binaryMap)} label={''} />

      <Text style={styles.label}>💼 Zihinsel sağlığınız iş performansınızı ne sıklıkla etkiliyor?</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={workInterfere}
          onValueChange={setWorkInterfere}
          style={Platform.OS === 'ios' ? styles.pickerIOS : styles.pickerAndroid}
          mode="dropdown"
        >
          <Picker.Item label="Seçiniz" value="" color="#999" />
          {workInterfereOptions.map(option => (
            <Picker.Item key={option.value} label={option.label} value={option.value} color="#000" />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>👥 Çalıştığınız şirketin büyüklüğü nedir?</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={noEmployees}
          onValueChange={setNoEmployees}
          style={Platform.OS === 'ios' ? styles.pickerIOS : styles.pickerAndroid}
          mode="dropdown"
        >
          <Picker.Item label="Seçiniz" value="" color="#999" />
          {employeeRanges.map(range => (
            <Picker.Item key={range.value} label={range.label} value={range.value} color="#000" />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>🎁 Zihinsel sağlık için ek faydalar (programlar) var mı?</Text>
      <RadioGroup options={binaryOptions.map(opt => opt.label)} selected={benefits} onSelect={(value) => setBenefits(value as keyof typeof binaryMap)} label={''} />

      <Text style={styles.label}>🕵️‍♀️ Destek alırken anonim kalabiliyor musunuz?</Text>
      <RadioGroup options={binaryOptions.map(opt => opt.label)} selected={anonymity} onSelect={(value) => setAnonymity(value as keyof typeof binaryMap)} label={''} />

      <Text style={styles.label}>👥 Çalışma arkadaşlarınızdan zihinsel sağlık konusunda destek alabiliyor musunuz?</Text>
      <RadioGroup
        label=""
        options={Object.keys(coworkersMap)}
        selected={coworkers}
        onSelect={(value) => setCoworkers(value as keyof typeof coworkersMap)}
      />

      <Text style={styles.label}>🧑‍💼 Yöneticinizden (supervisor) zihinsel sağlık konusunda destek alabiliyor musunuz?"</Text>
      <RadioGroup
        label=""
        options={Object.keys(supervisorMap)}
        selected={supervisor}
        onSelect={(value) => setSupervisor(value as keyof typeof supervisorMap)}
      />

      {/* <Text style={styles.label}>🗓️ Zihinsel sağlık nedeniyle izin almak ne kadar kolay?</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={leave}
          onValueChange={setLeave}
          style={Platform.OS === 'ios' ? styles.pickerIOS : styles.pickerAndroid}
          mode="dropdown"
        >
          <Picker.Item label="Seçiniz" value="" color="#999" />
          {leaveOptions.map(option => (
            <Picker.Item key={option.value} label={option.label} value={option.label} color="#000" />
          ))}
        </Picker>
      </View> */}

      <TouchableOpacity style={styles.customButton} onPress={handleSubmit}>
        <Text style={styles.buttonText}>🔮 Tahmin Et</Text>
      </TouchableOpacity>

      {error !== '' && <Text style={styles.error}>❌ {error}</Text>}

      {result && !result.error && (
        <View style={[styles.result, { backgroundColor: result.prediction === 1 ? '#f8d7da' : '#d4edda' }]}>
          <Text style={[styles.resultText, { color: result.prediction === 1 ? '#721c24' : '#155724' }]}>
            {result.prediction === 1 ? '💥 Destek Gerekli' : '✅ Destek Gerekmiyor'}
          </Text>
          <Text>Olasılık: %{Math.round((result.probability ?? 0) * 100)}</Text>
        </View>
      )}

      {result?.error && <Text style={styles.error}>❌ Hata: {result.error}</Text>}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#fff', flexGrow: 1 },
  title: { margin: 46, fontSize: 26, fontWeight: 'bold', marginBottom: 30, textAlign: 'center', color: '#333' },
  input: {
    borderWidth: 1, borderColor: '#aaa', borderRadius: 6, padding: 10, marginBottom: 12,
    backgroundColor: '#f9f9f9', color: '#000'
  },
  label: { marginTop: 10, fontWeight: 'bold' },
  radioGroup: { marginBottom: 10 },
  radioOptions: { flexDirection: 'row', flexWrap: 'wrap', gap: 15 },
  radioButton: { flexDirection: 'row', alignItems: 'center', marginRight: 10 },
  radioCircle: { width: 18, height: 18, borderRadius: 10, borderWidth: 1, borderColor: '#333', marginRight: 6, alignItems: 'center', justifyContent: 'center' },
  radioDot: { width: 10, height: 10, borderRadius: 5, backgroundColor: '#333' },
  pickerContainer: {
    borderWidth: 1, borderColor: '#aaa', borderRadius: 6, marginBottom: 12,
    backgroundColor: '#f9f9f9', overflow: 'hidden'
  },
  pickerIOS: { height: 200, width: '100%', backgroundColor: '#f9f9f9', color: '#000' },
  pickerAndroid: { height: 50, width: '100%', color: '#000' },
  result: { marginTop: 20, padding: 15, borderRadius: 6 },
  resultText: { fontSize: 18, fontWeight: 'bold' },
  error: { color: 'red', marginTop: 15, fontWeight: 'bold' },
  customButton: {
    backgroundColor: '#007bff',
    paddingVertical: 14,
    paddingHorizontal: 30,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold'
  }
});
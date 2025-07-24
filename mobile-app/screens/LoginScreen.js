import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { loginUser } from "../services/authService";
import { validateEmail } from "../utils/validation";

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!validateEmail(email)) {
      return setError("Invalid email format.");
    }

    const result = await loginUser(email, password);
    if (result.success) {
      setError("");
      navigation.navigate("Home", { userId: result.data.user_id });
    } else {
      setError(result.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        autoCapitalize="none"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Button title="Login" onPress={handleLogin} />
      <Text style={styles.link} onPress={() => navigation.navigate("Register")}>
        Don't have an account? Register
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  input: { borderBottomWidth: 1, marginBottom: 12, padding: 8 },
  title: { fontSize: 24, marginBottom: 20, textAlign: "center" },
  error: { color: "red", marginBottom: 10 },
  link: { marginTop: 20, color: "blue", textAlign: "center" },
});

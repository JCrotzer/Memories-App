import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { registerUser } from "../services/authService";
import { validateEmail, validatePassword } from "../utils/validation";

export default function RegisterScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleRegister = async () => {
    if (!validateEmail(email)) {
      return setError("Please enter a valid email address.");
    }
    if (!validatePassword(password)) {
      return setError("Password must be at least 8 characters long.");
    }

    const result = await registerUser(email, password);
    if (result.success) {
      setSuccess("Registration successful. You can now log in.");
      setError("");
      setEmail("");
      setPassword("");
      setTimeout(() => navigation.navigate("Login"), 1500);
    } else {
      setError(result.message);
      setSuccess("");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Register</Text>
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
      {success ? <Text style={styles.success}>{success}</Text> : null}
      <Button title="Register" onPress={handleRegister} />
      <Text style={styles.link} onPress={() => navigation.navigate("Login")}>
        Already have an account? Log in
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  input: { borderBottomWidth: 1, marginBottom: 12, padding: 8 },
  title: { fontSize: 24, marginBottom: 20, textAlign: "center" },
  error: { color: "red", marginBottom: 10 },
  success: { color: "green", marginBottom: 10 },
  link: { marginTop: 20, color: "blue", textAlign: "center" },
});

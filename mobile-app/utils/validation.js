// Simple email regex (can be improved as needed)
export const validateEmail = (email) => {
  const re = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
  return re.test(email);
};

// Password: min 8 chars, at least one uppercase, one lowercase, one number, one special char
export const validatePassword = (password) => {
  const re =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=\-{}[\]|:;"'<>,.?/]).{8,}$/;
  return re.test(password);
};

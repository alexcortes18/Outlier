function isValidEmail(email) {
    // Revisa si tiene longitud minima de 6, si contiene "@" y si contiene ".com"
    if (email.length < 6 || !email.includes('@') || !email.includes('.com')) {
      return false;
    }
    return true;
  }
  
  function isValidPassword(password) {
    // Revisa si la contraseña es de 8 carácteres mínimo.
    if (password.length < 8) {
      return false;
    }
  
    // Con el .test chequiamos si hay al menos 1 uppercase o 1 simbolo en cada regex que estamos testing.
    const hasUppercase = /[A-Z]/.test(password);
    const hasSymbol = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
    return hasUppercase && hasSymbol;
  }
  
  // Funcion para validar ambas cosas, email y password, y notificar al usuario si fue un éxito o no la validación.
  function validateUser(email, password) {
    const isEmailValid = isValidEmail(email);
    const isPasswordValid = isValidPassword(password);
  
    // La notificación al usuario se hace así porque no queremos dar alguna pista (clue) de que el usuario esta bien
    // y la contraseña no, por evitar que otras personas intenten acceder a un usuario que no es de ellos.
    if (isEmailValid && isPasswordValid) {
      return "Valid email and password!";
    } else {
      return "Invalid email or password.";
    }
  }

// ------------------------------------------------------------------------------------------------
// TEST CASES
// console.log("Test cases for emails:")
// Casos válidos
// console.log(isValidEmail('user@example.com')); // true
// console.log(isValidEmail('longer-user@example.com')); // true

// // Casos con longitud mínima inválida
// console.log(isValidEmail('us@example.com')); // false
// console.log(isValidEmail('@example.com')); // false
// console.log(isValidEmail('user.com')); // false

// // Casos sin "@"
// console.log(isValidEmail('user.example.com')); // false
// console.log(isValidEmail('user@example')); // false

// // Casos sin ".com"
// console.log(isValidEmail('user@example.org')); // false
// console.log(isValidEmail('user@example')); // false

// // Casos con caracteres especiales y formateos extraños
// console.log(isValidEmail('user+tag@example.com')); // true - Los '+' son válidos en correos electrónicos
// console.log(isValidEmail('user.with.dots@example.com')); // true - Los '.' son válidos antes del '@'
// console.log(isValidEmail('user@sub.domain.example.com')); // true - Subdominios válidos
// console.log(isValidEmail('"quoted user"@example.com')); // true - Las comillas son válidas en ciertos casos
  
// // console.log("Test cases for passwords:")

// // Casos válidos
// console.log(isValidPassword('Password1!')); // true
// console.log(isValidPassword('A1b2c3D4!@')); // true

// // Casos con longitud inválida
// console.log(isValidPassword('Pass1')); // false
// console.log(isValidPassword('Password')); // false

// // Casos sin letras mayúsculas
// console.log(isValidPassword('password1!')); // false
// console.log(isValidPassword('123456!@')); // false

// // Casos sin símbolos
// console.log(isValidPassword('Password1')); // false
// console.log(isValidPassword('A1b2c3D4')); // false

// // Casos con otros caracteres especiales válidos
// console.log(isValidPassword('Passw0rd@#')); // true
// console.log(isValidPassword('P@ssw0rd!')); // true

// // Casos límite
// console.log(isValidPassword('aaaaaaA1!')); // true - Longitud mínima con requisitos cumplidos

// // console.log("Test Cases for users:")

// // Casos válidos
// console.log(validateUser('user@example.com', 'Password1!')); // "¡Correo electrónico o contraseña válidos!"

// // Casos inválidos
// console.log(validateUser('us@example.com', 'Password1!')); // "¡Correo electrónico o contraseña no válidos!"
// console.log(validateUser('user@example.com', 'password1')); // "¡Correo electrónico o contraseña no válidos!"

// Casos válidos
console.log("Email: user@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('user@example.com')); // true
console.log("Email: longer-user@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('longer-user@example.com')); // true

// Casos con longitud mínima inválida
console.log("Email: us@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('us@example.com')); // true
console.log("Email: @example.com, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('@example.com')); // false
console.log("Email: user.com, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('user.com')); // false

// Casos sin "@"
console.log("Email: user.example.com, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('user.example.com')); // false
console.log("Email: user@example, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('user@example')); // false

// Casos sin ".com"
console.log("Email: user@example.org, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('user@example.org')); // false
console.log("Email: user@example, ", "Expected Result: false, ", "Actual Result: ", isValidEmail('user@example')); // false

// Casos con caracteres especiales y formateos extraños
console.log("Email: user+tag@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('user+tag@example.com')); // true - Los '+' son válidos en correos electrónicos
console.log("Email: user.with.dots@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('user.with.dots@example.com')); // true - Los '.' son válidos antes del '@'
console.log("Email: user@sub.domain.example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('user@sub.domain.example.com')); // true - Subdominios válidos
console.log("Email: \"quoted user\"@example.com, ", "Expected Result: true, ", "Actual Result: ", isValidEmail('"quoted user"@example.com')); // true - Las comillas son válidas en ciertos casos

// Casos válidos
console.log("Password: Password1!, ", "Expected Result: true, ", "Actual Result: ", isValidPassword('Password1!')); // true
console.log("Password: A1b2c3D4!@, ", "Expected Result: true, ", "Actual Result: ", isValidPassword('A1b2c3D4!@')); // true

// Casos con longitud inválida
console.log("Password: Pass1, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('Pass1')); // false
console.log("Password: Password, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('Password')); // false

// Casos sin letras mayúsculas
console.log("Password: password1!, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('password1!')); // false
console.log("Password: 123456!@, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('123456!@')); // false

// Casos sin símbolos
console.log("Password: Password1, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('Password1')); // false
console.log("Password: A1b2c3D4, ", "Expected Result: false, ", "Actual Result: ", isValidPassword('A1b2c3D4')); // false

// Casos con otros caracteres especiales válidos
console.log("Password: Passw0rd@#, ", "Expected Result: true, ", "Actual Result: ", isValidPassword('Passw0rd@#')); // true
console.log("Password: P@ssw0rd!, ", "Expected Result: true, ", "Actual Result: ", isValidPassword('P@ssw0rd!')); // true

// Casos límite
console.log("Password: aaaaaaA1!, ", "Expected Result: true, ", "Actual Result: ", isValidPassword('aaaaaaA1!')); // true - Longitud mínima con requisitos cumplidos

// Casos válidos
console.log("Email: user@example.com, Password: Password1!, ", "Expected Result: '¡Correo electrónico o contraseña válidos!', ", "Actual Result: ", validateUser('user@example.com', 'Password1!')); // "¡Correo electrónico o contraseña válidos!"

// Casos inválidos
console.log("Email: us@example.com, Password: Password1!, ", "Expected Result: '¡Correo electrónico o contraseña válidos!', ", "Actual Result: ", validateUser('us@example.com', 'Password1!')); // "¡Correo electrónico o contraseña válidos!"
console.log("Email: user@example.com, Password: password1, ", "Expected Result: '¡Correo electrónico o contraseña no válidos!', ", "Actual Result: ", validateUser('user@example.com', 'password1')); // "¡Correo electrónico o contraseña no válidos!"
console.log("Email: invalid@, Password: Password1!, ", "Expected Result: '¡Correo electrónico o contraseña no válidos!', ", "Actual Result: ", validateUser('invalid@', 'Password1!')); // "¡Correo electrónico o contraseña no válidos!"
console.log("Email: user@example, Password: Password1!, ", "Expected Result: '¡Correo electrónico o contraseña no válidos!', ", "Actual Result: ", validateUser('user@example', 'Password1!')); // "¡Correo electrónico o contraseña no válidos!"

// Casos límite
console.log("Email: user@example.com, Password: aaaaaaA1!, ", "Expected Result: '¡Correo electrónico o contraseña válidos!', ", "Actual Result: ", validateUser('user@example.com', 'aaaaaaA1!')); // "¡Correo electrónico o contraseña válidos!"
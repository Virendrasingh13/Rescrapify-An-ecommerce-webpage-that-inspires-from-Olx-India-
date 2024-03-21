// Get the JWT token from localStorage
const token = localStorage.getItem('access_token');

// Function to decode JWT token
function decodeToken(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
}

// Decode the JWT token
const decodedToken = decodeToken(token);

// Check if the token contains user information
if (decodedToken && decodedToken.user_id) {
    // User is logged in
    console.log(decodedToken)
    const currentUser = decodedToken.user;
    console.log('Current User:', currentUser);
    
    // Extract email from the user object
    // const email = currentUser.user.email;
    // console.log('Email:', email);
} else {
    // User is not logged in
    alert('Please log in to access this feature.');
}

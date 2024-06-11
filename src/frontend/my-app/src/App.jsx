import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [optionalField, setOptionalField] = useState('');
  const [dummyId, setDummyId] = useState('');
  const [response, setResponse] = useState(null);
  const [dummies, setDummies] = useState([]);
  const [updateMode, setUpdateMode] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [registerMode, setRegisterMode] = useState(false);
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');

  // Pobierz URL backendu z zmiennej środowiskowej
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'https://localhost:80';

  useEffect(() => {
    if (token) {
      fetchDummies();
    }
  }, [token]);

  const fetchDummies = async () => {
    try {
      const res = await axios.get(`${backendUrl}/api/dummy`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log('Fetched dummies:', res.data);
      setDummies(res.data);
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setDummies([]);
        console.log('No dummies found.');
      } else {
        console.error('Error fetching dummies:', err);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dummyData = {
      name,
      description,
      optional_field: optionalField || null,
    };
    console.log('Submitting form:', dummyData);

    try {
      let res;
      if (updateMode) {
        const url = `${backendUrl}/api/dummy/${dummyId}`;
        console.log('PUT URL:', url);
        console.log('PUT dummyId:', dummyId);
        res = await axios.put(url, dummyData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        const url = `${backendUrl}/api/dummy`;
        console.log('POST URL:', url);
        res = await axios.post(url, dummyData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      console.log('Response from server:', res.data);
      setResponse(res.data);
      fetchDummies();
      setName('');
      setDescription('');
      setOptionalField('');
      setDummyId('');
      setUpdateMode(false);
    } catch (err) {
      console.error('Error submitting form:', err);
    }
  };

  const handleEdit = (dummy) => {
    setName(dummy.name);
    setDescription(dummy.description);
    setOptionalField(dummy.optional_field || '');
    setDummyId(dummy.id);
    setUpdateMode(true);
    console.log('Edit mode set for dummy:', dummy);
    console.log('dummyId set to:', dummy.id);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${backendUrl}/api/dummy/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchDummies();
    } catch (err) {
      console.error('Error deleting dummy:', err);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${backendUrl}/api/auth/token`, new URLSearchParams({
        username,
        password,
      }));
      setToken(res.data.access_token);
      localStorage.setItem('token', res.data.access_token);
    } catch (err) {
      console.error('Error logging in:', err);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const userData = {
      username,
      email,
      full_name: fullName,
      password,
      disabled: false,
    };
    console.log('Registering user with data:', userData);

    try {
      const res = await axios.post(`${backendUrl}/api/auth/users/`, userData);
      console.log('User registered successfully:', res.data);
      setRegisterMode(false);
    } catch (err) {
      console.error('Error registering user:', err);
      if (err.response) {
        console.error('Server response:', err.response.data);
      }
    }
  };

  const handleLogout = () => {
    setToken('');
    setUsername('');
    setPassword('');
    localStorage.removeItem('token');
  };

  return (
    <div>
      <h1>Simple Vite and FastAPI App</h1>
      <div className="subtitle">
        <h2>Source: <a href="https://github.com/ozieblo-michal/fastAPI-engine">fastAPI-engine</a></h2>
        <a href="https://github.com/ozieblo-michal/fastAPI-engine">
          <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" className="github-icon" />
        </a>
      </div>
      
      {!token ? (
        <>
          {registerMode ? (
            <form onSubmit={handleRegister}>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <input
                type="text"
                placeholder="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button className="primary" type="submit">Register</button>
              <button className="secondary" type="button" onClick={() => setRegisterMode(false)}>Back to Login</button>
            </form>
          ) : (
            <form onSubmit={handleLogin}>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button className="primary" type="submit">Login</button>
              <button className="secondary" type="button" onClick={() => setRegisterMode(true)}>Register</button>
            </form>
          )}
        </>
      ) : (
        <>
          <button className="secondary" onClick={handleLogout}>Logout</button>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              minLength={1}
              maxLength={100}
            />
            <input
              type="text"
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              minLength={1}
              maxLength={100}
            />
            <input
              type="text"
              placeholder="Optional Field"
              value={optionalField}
              onChange={(e) => setOptionalField(e.target.value)}
              maxLength={100}
            />
            <button className="primary" type="submit">{updateMode ? 'Update' : 'Submit'}</button>
          </form>
          {response && (
            <div>
              <h2>Response:</h2>
              {/* <p>ID: {response.id}</p> */}
              <p>Name: {response.name}</p>
              <p>Description: {response.description}</p>
              {response.optional_field && <p>Optional Field: {response.optional_field}</p>}
            </div>
          )}
          <h2>All Dummies</h2>
          <ul>
            {dummies.length > 0 ? (
              dummies.map((dummy) => (
                <li key={dummy.id}>
                  <p>ID: {dummy.id}</p>
                  <p>Name: {dummy.name}</p>
                  <p>Description: {dummy.description}</p>
                  {dummy.optional_field && <p>Optional Field: {dummy.optional_field}</p>}
                  <button className="primary" onClick={() => handleEdit(dummy)}>Edit</button>
                  <button className="secondary" onClick={() => handleDelete(dummy.id)}>Delete</button>
                </li>
              ))
            ) : (
              <p>No dummies available.</p>
            )}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;

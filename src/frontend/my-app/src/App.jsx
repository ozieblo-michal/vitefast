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
  const [selectedFile, setSelectedFile] = useState(null);
  const [s3Files, setS3Files] = useState([]);
  const [localFiles, setLocalFiles] = useState([]);

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'https://localhost:80';

  useEffect(() => {
    if (token) {
      fetchDummies();
      fetchS3Files();
      fetchLocalFiles();
    }
  }, [token]);

  const fetchDummies = async () => {
    try {
      const res = await axios.get(`${backendUrl}/dummy`, {
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

  const fetchS3Files = async () => {
    try {
      const res = await axios.get(`${backendUrl}/list_s3_files`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setS3Files(res.data.files);
    } catch (err) {
      console.error('Error fetching S3 files:', err);
    }
  };

  const fetchLocalFiles = async () => {
    try {
      const res = await axios.get(`${backendUrl}/list_local_files`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setLocalFiles(res.data.files);
    } catch (err) {
      console.error('Error fetching local files:', err);
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
        const url = `${backendUrl}/dummy/${dummyId}`;
        console.log('PUT URL:', url);
        console.log('PUT dummyId:', dummyId);
        res = await axios.put(url, dummyData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        const url = `${backendUrl}/dummy`;
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
      await axios.delete(`${backendUrl}/dummy/${id}`, {
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
      const res = await axios.post(`${backendUrl}/auth/token`, new URLSearchParams({
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
      const res = await axios.post(`${backendUrl}/auth/users/`, userData);
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

  const handleFileUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post(`${backendUrl}/uploads3`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('File uploaded successfully:', res.data);
      setSelectedFile(null);
      fetchS3Files();
    } catch (err) {
      console.error('Error uploading file:', err);
    }
  };

  const handleFileDelete = async (filename) => {
    try {
      await axios.delete(`${backendUrl}/delete_from_s3/${filename}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchS3Files();
    } catch (err) {
      console.error('Error deleting file from S3:', err);
    }
  };

  const handleLocalFileUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post(`${backendUrl}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('File uploaded locally successfully:', res.data);
      setSelectedFile(null);
      fetchLocalFiles();
    } catch (err) {
      console.error('Error uploading local file:', err);
    }
  };

  const handleLocalFileDelete = async (filename) => {
    try {
      await axios.delete(`${backendUrl}/delete_local_file/${filename}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchLocalFiles();
    } catch (err) {
      console.error('Error deleting local file:', err);
    }
  };

  const handleDownloadS3File = async (filename) => {
    try {
      const res = await axios.get(`${backendUrl}/download_s3/${filename}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error('Error downloading S3 file:', err);
    }
  };

  const handleDownloadLocalFile = async (filename) => {
    try {
      const res = await axios.get(`${backendUrl}/download/${filename}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error('Error downloading local file:', err);
    }
  };

  return (
    <div>
      <h1>Simple Vite and FastAPI App</h1>
      <h3 className="subtitle">
        Enforce HTTPS is required for this site because it uses the default domain (ozieblo-michal.github.io). This may be disabled if you switch to a custom domain. Open the link <a href={`${backendUrl}:81`} target="_blank" rel="noopener noreferrer">{`${backendUrl}:81/docs`}</a> and accept the self-signed certificate to ensure the frontend functions correctly.
      </h3>
      <div className="subtitle">
        <h2>Source: <a href="https://github.com/ozieblo-michal/vitefast">ViteFast</a></h2>
        <a href="https://github.com/ozieblo-michal/vitefast">
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

          <h2>Upload File to S3</h2>
          <form onSubmit={handleFileUpload}>
            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              required
            />
            <button className="primary" type="submit">Upload</button>
          </form>

          <h2>Upload File Locally</h2>
          <form onSubmit={handleLocalFileUpload}>
            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              required
            />
            <button className="primary" type="submit">Upload</button>
          </form>

          <h2>Local Files</h2>
          <ul>
            {localFiles.length > 0 ? (
              localFiles.map((file) => (
                <li key={file}>
                  <p>{file}</p>
                  <button className="secondary" onClick={() => handleDownloadLocalFile(file)}>Download</button>
                  <button className="secondary" onClick={() => handleLocalFileDelete(file)}>Delete</button>
                </li>
              ))
            ) : (
              <p>No local files available.</p>
            )}
          </ul>

          <h2>S3 Files</h2>
          <ul>
            {s3Files.length > 0 ? (
              s3Files.map((file) => (
                <li key={file}>
                  <p>{file}</p>
                  <button className="secondary" onClick={() => handleDownloadS3File(file)}>Download</button>
                  <button className="secondary" onClick={() => handleFileDelete(file)}>Delete</button>
                </li>
              ))
            ) : (
              <p>No files in S3.</p>
            )}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;

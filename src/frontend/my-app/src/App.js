import React, {useState, useEffect} from 'react';
import api from './api';

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    optional_field: ''
  });

  const fetchTransactions = async () => {
    const response = await api.get('/dummy');
    setTransactions(response.data);
  }

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({...formData, [event.target.name]: value});
  }

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/dummy', formData);
    fetchTransactions();
    setFormData({name: '', description: '', optional_field: ''});
  };

  return (
    <div>
      <h1>Transactions</h1>
      <form onSubmit={handleFormSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={formData.name} onChange={handleInputChange} />
        </label>
        <label>
          Description:
          <input type="text" name="description" value={formData.description} onChange={handleInputChange} />
        </label>
        <label>
          Optional Field:
          <input type="text" name="optional_field" value={formData.optional_field} onChange={handleInputChange} />
        </label>
        <button type="submit">Submit</button>
      </form>
      <ul>
        {transactions.map(transaction => (
          <li key={transaction.id}>
            {transaction.name} - {transaction.description} - {transaction.optional_field}
          </li>
        ))}
      </ul>
      <button onClick={fetchTransactions}>Refresh</button>
      <button onClick={() => api.delete('/dummy')}>Delete All</button>
    </div>
  )

}


export default App;

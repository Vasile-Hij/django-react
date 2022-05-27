import './App.css';
import { BrowserRouter as Router, Route} from "react-router-dom";
import PrivateRoute from './utils/PrivateRoute'
import { AuthProvider } from './context/AuthContext'

import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import Header from './components/Header'


function App() {
  return ( 
    <div className="App">
      <Router>
        <AuthProvider>
          <Header/>
          <PrivateRoute path="/" exact component={HomePage} />
          <Route path="/login" component={LoginPage} />
        </AuthProvider>
      </Router>
    </div>      
  );
}

export default App;
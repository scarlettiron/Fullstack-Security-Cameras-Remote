import './App.css';
import React from 'react'
import { BrowserRouter as Router, Route} from 'react-router-dom';
import PrivateRoute from './PrivateRoute'
import {AuthProvider} from './context/AuthContext'
import {SocketProvider} from './context/SocketContext'
import { DeviceProvider } from './context/DeviceContext';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Home from './pages/Home'
import CameraStream from './pages/CameraStream';
import Alerts from './pages/Alerts';
import AddDevice from './pages/AddDevice';
import EditDevice from './pages/EditDevice';
import EditHousehold from './pages/EditHousehold';
import AddAllowedPerson from './pages/AddAllowedPerson';
import AddServer from './pages/AddServer';
import EditServer from './pages/EditServer';


function App() {

  return (
    <div className="App">
      <Router>
      <AuthProvider>
        <Route exact component={Login} path='/'></Route>
        <Route component={Login} path='/login'></Route>
        <Route component={Signup} path='/signup'></Route>
          <DeviceProvider>
            <SocketProvider>
              <PrivateRoute component={Home} path='/home'/>
              <PrivateRoute component={CameraStream} path='/camera/:unit_id'/>
              <PrivateRoute component={Alerts} path='/alerts'/>
              <PrivateRoute component={AddDevice} path='/add-device'/>
              <PrivateRoute component={EditDevice} path='/edit/:unit_id'/>
              <PrivateRoute component={EditHousehold} path='/edithousehold'/>
              <PrivateRoute component={AddAllowedPerson} path='/add-allowed-person'/>
              <PrivateRoute component={AddServer} path='/add-server'/>
              <PrivateRoute component={EditServer} path='/edit-server/:unit_id'/>
            </SocketProvider>
          </DeviceProvider>
        </AuthProvider>
      </Router>
      
    </div>
  );
}

export default App;

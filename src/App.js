import React from 'react';
import logo from './logo.svg';
import { Counter } from './features/counter/Counter';
import './App.css';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";
import Container from "react-bootstrap/Container";
import AboutPage from "./pages/AboutPage";
import LandingPage from "./pages/LandingPage";


function App() {
  return (
    <div className="App">
        <Router>
          <Container>
            <Switch>
              <Route path={"/about"}>
                  <AboutPage/>
              </Route>
              <Route path={"/"}>
                <LandingPage/>
              </Route>
            </Switch>
          </Container>
        </Router>

    </div>
  );
}

export default App;

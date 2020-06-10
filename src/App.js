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
import Header from "./components/Header";

let firebase_obj = require('./components/Firestore');

function App() {
    /*
    firebase_obj.database.collection("users").doc("Momina").set({
        first: "Ada",
        last: "Lovelace",
        born: 1815
    })
        .then(function(docRef) {
            console.log("Document written with ID: ", docRef.id);
        })
        .catch(function(error) {
            console.error("Error adding document: ", error);
        });

     */
    //let ref = firebase_obj.firestore.create_query_doc('racism');
    //firebase_obj.firestore.add_query_pdf("","new.pdf","racism");



    return (
        <Router>
            <Header/>
            <div className="App">
                <Container fluid>
                    <Switch>
                        <Route path={"/about"}>
                            <AboutPage/>
                        </Route>
                        <Route path={"/"}>
                            <LandingPage/>
                        </Route>
                    </Switch>
                </Container>
            </div>
        </Router>


    );
}

export default App;

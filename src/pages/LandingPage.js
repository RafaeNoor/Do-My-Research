import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";


class LandingPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'currentTime':0,
        };
        
    }

    componentDidMount() {
        fetch('/time').then(res => res.json()).then(data => {
            console.log(data)
            this.setState({'currentTime':data.time});
        });
    }


    render() {
        return (
            <div>
                <Container>
                    <h1>Landing Page!</h1>
                    <p>The current time is {this.state.currentTime}</p>
                </Container>
            </div>
        );
    }
}

export default LandingPage;

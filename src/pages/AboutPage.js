import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";


class AboutPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }


    render() {
        return (
            <div>
                <Container fluid>
                    <h1>About Page!</h1>
                </Container>
            </div>
        );
    }
}

export default AboutPage;

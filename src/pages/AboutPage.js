import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";
import Figure from "react-bootstrap/Figure";
import Row from "react-bootstrap/Row";
import Card from "react-bootstrap/Card";


class AboutPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "LinkedIn":"https://www.linkedin.com/in/abdul-rafae-noor-a8ba5119a/",
            "GitHub":"https://github.com/RafaeNoor",
            "GMail":"mailto:rafaenoor98@gmail.com",

        };
    }

    render() {
        let links = [];
        Object.keys(this.state).forEach(contact =>{
            links.push(<a href={this.state[contact]} target="_blank">{contact}</a>);
            links.push(<br/>)
        })
        return (
            <div>
                <Container fluid>
                    <h1>About Page!</h1>
                    <Row className={"justify-content-md-center"}>
                        <Card border={"light"} bg={"dark"} text={"white"}>
                            <Card.Header><h5>Abdul Rafae Noor</h5></Card.Header>
                            <Card.Body>
                            <Figure>
                                <Figure.Image
                                    roundedCircle
                                    src={'rafae.jpeg'}
                                    width={300}
                                    height={300}
                                />
                                <Figure.Caption>

                                    <p className={"white_text_style"}>This application was developed by Abdul Rafae Noor, B.S. Computer<br/> Science from
                                    Lahore University of Management Sciences (LUMS). This<br/> project was inspired after a
                                    course project at LUMS, where<br/> Rafae noticed how his entire labour could be automated<br/>
                                        if given some time. Hence here are the results.</p>
                                </Figure.Caption>

                            </Figure>
                            </Card.Body>
                            <Card.Footer>{links}</Card.Footer>
                        </Card>
                    </Row>

                </Container>
            </div>
        );
    }
}

export default AboutPage;

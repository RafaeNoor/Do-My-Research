import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";
import Header from "../components/Header";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";


class LandingPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'currentTime':0,
            'text':"",
            'summary':"",
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
                <Container fluid>

                    <h1>Landing Page!</h1>
                    <p>The current time is {this.state.currentTime}</p>
                    <Form.Group>
                        <Form.Control size="lg" type="text" placeholder="Enter URL to summarize" onChange={
                            e=>this.state.text = (e.target.value)} />

                        <Button onClick={() => {
                            console.log(this.state.text);
                            fetch(`/summary/${this.state.text}`).then(res => res.json()).then(data => {
                                console.log(data)
                                this.setState({'summary':data.summary});
                            });

                        }
                        }>Submit</Button>
                    </Form.Group>
                    {this.state.summary}

                </Container>
            </div>
        );
    }
}

export default LandingPage;

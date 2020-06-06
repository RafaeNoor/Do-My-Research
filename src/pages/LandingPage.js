import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";
import Header from "../components/Header";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Table from "react-bootstrap/Table";
import TwitterAnalysisResults from "../components/TwitterAnalysisResults";


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

    createTable(json_obj){
        //json_obj = JSON.parse(json_obj);
        let uids = Object.keys(json_obj)

        let field_names = Object.keys(json_obj[uids[0]])

        let table_rows = []

        uids.forEach(uid => {
            let entry = json_obj[uid];
            let table_fields = [];

            field_names.forEach(field => {
                table_fields.push(<td>{entry[field]}</td>);
            })
            let row = (
                <tr>
                    {table_fields}
                </tr>
            );

            table_rows.push(row);
        });

        let table_header = [];

        field_names.forEach(field => {
            table_header.push(<th>{field}</th>);
        })
        return (
            <Table striped bordered hover variant="dark">
                <thead>
                <tr>
                    {table_header}
                </tr>
                </thead>
                <tbody>
                {table_rows}
                </tbody>
            </Table>

        );
    }


    render() {
        return (
            <div>
                <Container fluid>

                    <Row className="justify-content-md-center">
                        <h1>Landing Page!</h1>
                    </Row>
                    <Row className="justify-content-md-center">
                        <p>The current time is {this.state.currentTime}</p>
                    </Row>
                    <Form.Group>
                        <Row className="justify-content-md-center">
                            <Col>
                                <Form.Control size="lg" type="text" placeholder="Enter URL to summarize" onChange={
                                    e=>this.state.text = (e.target.value)} />
                            </Col>
                            <Col md={"auto"}>

                                <Button onClick={() => {
                                    console.log(this.state.text);
                                    fetch(`/summary/${this.state.text}`).then(res => res.json()).then(data => {
                                        console.log(data)
                                        this.setState({'summary':data.summary});
                                    });
                                }
                                }>Submit</Button>
                            </Col>
                        </Row>
                        <br/>
                        <Row className="justify-content-md-center">
                            <Col>
                                <Form.Control size="lg" type="text" placeholder="Enter PHRASE to Google" onChange={
                                    e=>this.state.text = (e.target.value)} />
                            </Col>
                            <Col md={"auto"}>

                                <Button onClick={() => {
                                    console.log(this.state.text);
                                    fetch(`/search/${this.state.text}`).then(res => res.json()).then(data => {
                                        console.log(JSON.stringify(data));
                                        let items = data.items
                                        let urls = []
                                        items.forEach(item => {
                                            urls.push(item.formattedUrl);
                                        })

                                        console.log(urls)

                                        this.setState({'summary':JSON.stringify(urls,null,4)});
                                    });
                                }
                                }>Submit</Button>
                            </Col>
                        </Row>
                        <br/>
                        <Row className="justify-content-md-center">
                            <Col>
                                <Form.Control size="lg" type="text" placeholder="Enter phrase to process tweet" onChange={
                                    e=>this.state.text = (e.target.value)} />
                            </Col>
                            <Col md={"auto"}>

                                <Button onClick={() => {
                                    console.log(this.state.text);
                                    console.log('Check');
                                    fetch(`/tweet_search/${this.state.text}`).then(res => res.json()).then(data => {
                                        //this.setState({'summary':this.createTable(data.data)});//JSON.stringify(data,null,4)});
                                        //console.log(data.file_paths)
                                        let component = (
                                            <Container fluid>
                                                <TwitterAnalysisResults table_data={data.data} file_paths={data.file_paths} />
                                            </Container>

                                        );
                                        this.setState({'summary':component});
                                    });
                                }
                                }>Submit</Button>
                            </Col>
                        </Row>

                    </Form.Group>
                    {this.state.summary}

                </Container>
            </div>
        );
    }
}

export default LandingPage;

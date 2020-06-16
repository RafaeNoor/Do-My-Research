import React from "react";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import GoogleTrendsAnalysisResults from "./GoogleTrendsAnalysisResults";
import Card from "react-bootstrap/Card";

//import 'bootstrap/dist/css/bootstrap.min.css';
class RedditAnalysisResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "phrase": props.phrase || "NO_PHRASE_PROVIDED",
            "analysis_obj": props.analysis_obj || {},
        };
    }

    createTable(json_obj){
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

    createImage(filepaths){
        let component = (
            <div>
                <Row className={"justify-content-md-center"}>
                    <Col md={'auto'}>
                        <Image rounded fluid src={filepaths[0]}></Image>
                    </Col>
                    <Col md ={'auto'}>
                        <Image rounded fluid src={filepaths[1]}></Image>
                    </Col>
                </Row>
                <br/>
                <Row className={"justify-content-md-center"}>
                    <Card>
                        <Card.Header as="h5">{"Sentiment Analysis of Reddit Posts"}</Card.Header>
                        <Card.Body>{"Sample Description"}</Card.Body>
                        <Card.Footer>Analysis using Reddit</Card.Footer>
                    </Card>
                </Row>
                <br/>
            </div>
        );

        return component
    }



    render() {
        return (
            <div>
                <Container fluid>
                    <h1>Reddit Analysis Result!</h1>
                    <br/>
                    {this.createTable(this.state.analysis_obj.table_data)}
                    {this.createImage(this.state.analysis_obj.file_paths)}
                </Container>
            </div>
        );
    }
}

export default RedditAnalysisResults;

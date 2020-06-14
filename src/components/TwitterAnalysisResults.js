import React from "react";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import GoogleTrendsAnalysisResults from "./GoogleTrendsAnalysisResults";
import Card from "react-bootstrap/Card";

//import 'bootstrap/dist/css/bootstrap.min.css';
class TwitterAnalysisResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "table_data": props.table_data || {},
            "file_paths": props.file_paths || [],
            "analysis_obj": props.analysis_obj || {},
        };

        console.log(props.file_paths);
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

    createImages(filepaths){

        let components = []

        let location_component = (
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
                <Card border={"dark"} bg={'dark'} text={'white'}>
                    <Card.Header as="h5">{"Geographical Analysis"}</Card.Header>
                    <Card.Body>{this.state.analysis_obj.desc}</Card.Body>
                </Card>
            </Row>
                <br/>
            </div>
        );

        let sentiment_component = (
            <Row className={"justify-content-md-center"}>
                <Col md={'auto'}>
                    <Image rounded src={filepaths[2]}></Image>
                </Col>
                <Col md ={'auto'}>
                    <Image rounded src={filepaths[3]}></Image>
                </Col>

            </Row>
        );

        components = [location_component,<br/>,sentiment_component];

        /*filepaths.forEach(fp => {
            components.push(
            <Row className={"justify-content-md-center"}>
                <Image src={fp}></Image>
            </Row>
            );
        });*/
        return components;
    }


    render() {
        //<GoogleTrendsAnalysisResults analysis_obj={this.state.analysis_obj.google} phrase={'Locations'}/>
        return (
            <div>
                <Container fluid>
                    <h2>Twitter Analysis Result!</h2>
                    <br/>
                    {this.createTable(this.state.table_data)}
                    {this.createImages(this.state.file_paths)}
                    <br/>
                    <GoogleTrendsAnalysisResults mode={"location"} analysis_obj={this.state.analysis_obj.google} phrase={'Locations'}/>
                    <br/>
                </Container>
            </div>
        );
    }
}

export default TwitterAnalysisResults;

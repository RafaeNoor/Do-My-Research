import React from "react";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Figure from "react-bootstrap/Figure";
import Card from "react-bootstrap/Card";

//import 'bootstrap/dist/css/bootstrap.min.css';
class GoogleTrendsAnalysisResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "file_paths": props.file_paths || [],
            "analysis_obj": props.analysis_obj || {},
            "phrase": props.phrase || "NO_PHRASE_SPECIFIED",
            "mode": props.mode || "trends"
        };

        console.log('CREATED TREND RESULT')

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
        filepaths.forEach(fp => {
            components.push(
                <Row className={"justify-content-md-center"}>
                    <Image src={fp}></Image>
                </Row>
            );
        });
        return components;
    }

    createEntry(type){

        let top_entries = [];

        let title = "";
        let key = "";

        if(type == "top"){
            title = `Top Trending Related Terms for ${this.state.phrase} across all time`
            key = "top"
        } else if(type == "rising") {
            title = `Top Trending Related Terms for ${this.state.phrase} as of ${new Date().toDateString()}`;
            key = 'rising';
        } else if(type == "location"){
            title = `Top Trending locations for ${this.state.phrase} according to Twitter Analysis`;
            key = 'location';

        }
        //console.log("ANALYSIS OBJ")
        //console.log(this.state.analysis_obj)

        let counter = 0;
        console.log(this.state);
        console.log(this.state.analysis_obj);
        this.state.analysis_obj[key].forEach(search_obj => {
            let search_term = Object.keys(search_obj)[0];
            console.log(search_obj)
            console.log(search_term)

            let left= "";
            let right = "";

            let card = (<Col>
                <Card>
                    <Card.Header as="h5">{search_term}</Card.Header>
                    <Card.Body>{search_obj[search_term]['summary']}
                    </Card.Body>
                    <Card.Footer><a href={search_obj[search_term]['citation']} target={"_blank"}>{search_term + " citation"}</a></Card.Footer>
                </Card>

            </Col>);
            let figure = (<Col md={"auto"}>
                <Figure>
                    <Figure.Image
                        rounded
                        width={600}
                        height={600}
                        src={search_obj[search_term]['img']}
                        alt={`Image describing ${search_term}`}
                    />
                </Figure>
            </Col>);
            counter += 1;
            if(counter % 2 == 0){
                left = figure;
                right = card;
            } else {
                left = card;
                right = figure;

            }

            //<h3>{search_term}</h3><br/>
            top_entries.push(
                <div>
                    <Row>
                        {left}
                        {right}
                    </Row>
                    <br/>
                </div>
            );
        })

        let result = (
            <Container fluid>
                <h2>{title}</h2>
                {top_entries}
            </Container>
        );

        return result;

    }


    render() {
        if(this.state.mode == "trends") {
            return (
                <div>
                    <Container fluid>
                        <h1>Google Trend Analysis!</h1>
                        {this.createEntry('top')}
                        <br/>
                        {this.createEntry('rising')}
                    </Container>
                </div>
            );
        } else if(this.state.mode == "location") {
            return (
                <div>
                    <Container fluid>
                        <h1>Google Trend Analysis!</h1>
                        {this.createEntry('location')}
                    </Container>
                </div>
            );

        }
    }
}

export default GoogleTrendsAnalysisResults;
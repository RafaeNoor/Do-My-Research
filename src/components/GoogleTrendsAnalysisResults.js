import React from "react";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Figure from "react-bootstrap/Figure";

//import 'bootstrap/dist/css/bootstrap.min.css';
class GoogleTrendsAnalysisResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "file_paths": props.file_paths || [],
            "analysis_obj": props.analysis_obj || {},
            "phrase": props.phrase || "NO_PHRASE_SPECIFIED",
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
        } else {
            title = `Top Trending Related Terms for ${this.state.phrase} as of ${new Date().toDateString()}`;
            key = 'rising';
        }
        //console.log("ANALYSIS OBJ")
        //console.log(this.state.analysis_obj)

        this.state.analysis_obj[key].forEach(search_obj => {
            let search_term = Object.keys(search_obj)[0];
            console.log(search_obj)
            console.log(search_term)


            top_entries.push(
            <Row>
                <h3>{search_term}</h3><br/>
                <Col md={'auto'}>
                {search_obj[search_term]['summary']}
                <a href={search_obj[search_term]['citation']}>{search_term + " citation"}</a>
                </Col>
                <Col md={'auto'}>
                    <Figure>
                        <Figure.Image
                            width={200}
                            height={200}
                            src={search_obj[search_term]['img']}
                            alt={`Image describing ${search_term}`}
                            />
                    </Figure>
                </Col>
            </Row>
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
    }
}

export default GoogleTrendsAnalysisResults;
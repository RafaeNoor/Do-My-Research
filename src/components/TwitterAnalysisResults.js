import React from "react";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";

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
        filepaths.forEach(fp => {
            components.push(
            <Row className={"justify-content-md-center"}>
                <Image src={fp}></Image>
            </Row>
            );
        });
        return components;
    }


    render() {
        return (
            <div>
                <Container fluid>
                    {this.createTable(this.state.table_data)}
                    {this.createImages(this.state.file_paths)}
                    {this.state.analysis_obj.desc}

                </Container>
            </div>
        );
    }
}

export default TwitterAnalysisResults;

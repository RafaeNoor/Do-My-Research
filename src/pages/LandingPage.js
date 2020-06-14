import React from "react";
import {LinkContainer } from 'react-router-bootstrap';
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Table from "react-bootstrap/Table";
import TwitterAnalysisResults from "../components/TwitterAnalysisResults";
import GoogleTrendsAnalysisResults from "../components/GoogleTrendsAnalysisResults";
import Spinner from "react-bootstrap/Spinner";

let firebase_obj = require('../components/Firestore');
let trend_obj = require('../components/GoogleTrends').trend_obj;


//let pdf = require('html-pdf');
let html2canvas = require('html2canvas')
let jsPdf = require('jspdf');

window.html2canvas = html2canvas

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

    async get_google_trend_results(phrase){
        let res = await trend_obj.get_related_terms(phrase);
        return (<GoogleTrendsAnalysisResults
            analysis_obj={res} phrase={phrase} />);
    }

    async get_twitter_analysis_results(phrase){
        let links = await firebase_obj.firestore.get_phrase_csvs(phrase);
        //console.log(`Links: ${JSON.stringify(links)}`);
        let promises = [];
        links.forEach(link => {
            console.log(link)
            promises.push(fetch(`get_storage_urls/${phrase}/${link}`));
        });

        let value = await Promise.all(promises)
        console.log('All files downloaded!');
        let data = await fetch(`/tweet_search/${phrase}`).then(res => res.json());
        console.log(data.file_paths);
        let component = (
            <Container fluid>
                <TwitterAnalysisResults table_data={data.data} file_paths={data.file_paths} analysis_obj={data.analysis_obj}
                sent_geo_analysis_obj = {data.sent_geo_analysis_obj}/>
            </Container>

        );

        return component;

    }


    render() {
        return (
            <div>
                <Container fluid>
                    <br/>
                    <Row className="justify-content-md-center">
                        <h1>Do My Research!</h1>
                    </Row>
                    <br/>
                    <Form.Group>
                        <Row className="justify-content-md-center">
                            <Col>
                                <Form.Control size="lg" type="text" placeholder="Enter phrase to Research" onChange={
                                    e=>this.state.text = (e.target.value)} />
                            </Col>
                            <Col md={"auto"}>

                                <Button variant={"dark"} onClick={() => {
                                    this.setState({"summary":<Spinner animation={"border"} size={"lg"} /> })
                                    console.log(this.state.text);
                                    console.log('Checking related terms...');

                                    let get_all_results = [];

                                    get_all_results.push(this.get_twitter_analysis_results(this.state.text));
                                    get_all_results.push(this.get_google_trend_results(this.state.text));

                                    Promise.all(get_all_results).then(all_results => {
                                        this.setState({'summary':all_results});
                                    });


                                }
                                }>Submit</Button>
                            </Col>
                        </Row>

                    </Form.Group>
                    <Button variant={"dark"} onClick={evt => {
                        //let html = document.getElementsByTagName('html')[0]
                        console.log('printing html')
                        //console.log(JSON.stringify(document));
                        let html_str = new XMLSerializer().serializeToString(document);
                        //let html = fs.readFileSync('index.html','utf8');
                        /*fetch(`/read_html/${html_str}`).then(res => res.json()).then(data => {
                            console.log('new file created');
                        });*/
                        //////////////////window.print();
                        //save_pdf();
                        //pdf.create(html_str).toFile('out.pdf',()=>{});
                        alert('Yet to implement properly, why not use your browsers in the meal while!')
                        window.print();







                    }}>Save PDF</Button>
                    <br/>
                    <br/>
                    {this.state.summary}

                </Container>
            </div>
        );
    }
}


function downloadBlob(blob, filename) {
    // Create an object URL for the blob object
    const url = URL.createObjectURL(blob);

    // Create a new anchor element
    const a = document.createElement('a');

    // Set the href and download attributes for the anchor element
    // You can optionally set other attributes like `title`, etc
    // Especially, if the anchor element will be attached to the DOM
    a.href = url;
    a.download = filename || 'download';

    // Click handler that releases the object URL after the element has been clicked
    // This is required for one-off downloads of the blob content
    const clickHandler = () => {
        setTimeout(() => {
            URL.revokeObjectURL(url);
            //this.removeEventListener('click', clickHandler);
        }, 150);
    };

    // Add the click event listener on the anchor element
    // Comment out this line if you don't want a one-off download of the blob content
    a.addEventListener('click', clickHandler, false);

    // Programmatically trigger a click on the anchor element
    // Useful if you want the download to happen automatically
    // Without attaching the anchor element to the DOM
    // Comment out this line if you don't want an automatic download of the blob content
    a.click();

    // Return the anchor element
    // Useful if you want a reference to the element
    // in order to attach it to the DOM or use it in some other way
    return a;
}

export default LandingPage;





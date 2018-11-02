import React, { Component } from 'react'
import { Container, Row, Col, Input, Form } from 'reactstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


class Footer extends Component {
    constructor(props) {
        super(props)
        this.state = {
            input: ""
        }
    }

    onChange = (e) => {
        e.preventDefault()
        this.setState({
            input: e.target.value
        })
    }

    onSubmit = (e) => {
        e.preventDefault()
        const { input } = this.state
        if (input.length > 0) {
            this.props.onSubmit(input)
            this.setState({
                input: ""
            })
        }
    }
    
    render() {
        return (
            <footer className="footer">
                <Container>
                    <Row>
                        <Col xs="10">
                            <Form onSubmit={this.onSubmit}>
                                <Input onChange={this.onChange} value={this.state.input}/>
                            </Form>
                        </Col>
                        <Col xs="2">
                            <FontAwesomeIcon icon="arrow-alt-circle-right" size="2x" color="darkGreen" onClick={this.onSubmit}/>
                        </Col>
                    </Row>
                </Container>
            </footer>
        )
    }
}

export default Footer
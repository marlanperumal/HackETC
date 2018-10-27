import React from "react"

import { Row, Col, Alert } from 'reactstrap'

const LeftMessage = ({text}) => (
    <Row>
        <Col xs={{ size: 10 }}>
            <Alert color="light">
                {text}
            </Alert>
        </Col>
    </Row>
)

export default LeftMessage
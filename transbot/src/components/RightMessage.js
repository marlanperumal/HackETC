import React from "react"

import { Row, Col, Alert } from 'reactstrap'

const RightMessage = ({text}) => (
    <Row>
        <Col xs={{ size: 10, offset: 2 }}>
            <Alert color="success">
                {text}
            </Alert>
        </Col>
    </Row>
)

export default RightMessage
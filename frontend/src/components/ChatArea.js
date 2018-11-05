import React, { Component } from 'react'
import { Container } from 'reactstrap'

import Message from './Message' 


class ChatArea extends Component {
    scrollToBottom = () => {
        this.messagesEnd.scrollIntoView({ behavior: "smooth" });
    }

    componentDidMount() {
        this.scrollToBottom();
    }
    
    componentDidUpdate() {
        this.scrollToBottom();
    }

    render() {
        const { messages, typing} = this.props
        return (
            <div id="chat-area">
                <Container>
                    {messages.map((message, i) => (
                        <Message key={i} {...message}/>
                    ))}
                    {typing ? "UDrive is typing..." : " "}
                    <div style={{ float:"left", clear: "both" }}
                        ref={(el) => { this.messagesEnd = el;}}>
                    </div>
                </Container>
            </div>
        )
    }
}

export default ChatArea
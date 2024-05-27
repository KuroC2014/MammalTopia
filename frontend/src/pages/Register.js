import React, { useState, startTransition } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { useNavigate } from "react-router-dom";
import { UserOutlined, MailOutlined, LockOutlined } from '@ant-design/icons';
import { postRegister } from '../requests/api';

function Register() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigateTo = useNavigate();

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };
    
    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };
    
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        postRegister({
            username: username,
            email: email,
            password: password
        }).then((data) => {
            message.success(`User ${username} registered successfully!`);
        }).catch((err) => {
            message.error(`User failed to register!`);
        })
    };

    return (
        <Card title="Register" style={{ width: 400, height:360 }}>
            <Form>
                <Form.Item>
                    <Input
                        prefix={<UserOutlined />}
                        placeholder="Username"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                </Form.Item>
                <Form.Item>
                    <Input
                        prefix={<MailOutlined />}
                        placeholder="Email"
                        value={email}
                        onChange={handleEmailChange}
                    />
                </Form.Item>
                <Form.Item>
                    <Input.Password
                        prefix={<LockOutlined />}
                        placeholder="Password"
                        value={password}
                        onChange={handlePasswordChange}
                    />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" block onClick={handleSubmit}>
                        Register
                    </Button>
                </Form.Item>
            </Form>
            <Button type="link" onClick={e => {
                e.preventDefault();
                startTransition(() => {
                    navigateTo('/login');
                });
            }}>
                Login
            </Button>
        </Card>
    );
}

export default Register;
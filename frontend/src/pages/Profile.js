import React, { useState, useEffect, startTransition } from 'react';
import { Button, Card, Input, Modal, message } from 'antd';
import { useNavigate } from "react-router-dom";
import { changePassword, deleteAccount, findUser } from '../requests/api';
import { LOGIN_TOKEN } from '../constants';
import { parseLoginToken } from '../utils/CommonUtils';


function Profile() {

    const [username, setUsername] = useState(parseLoginToken().username);
    const [userId, setUserId] = useState(parseLoginToken().userId);
    const [email, setEmail] = useState(parseLoginToken().email);
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');

    const [showChangePassword, setShowChangePassword] = useState(false);
    const [showDeleteAccount, setShowDeleteAccount] = useState(false);

    const navigateTo = useNavigate();

    // useEffect(() => {
    //     findUser({
    //         username: username
    //     }).then((data) => {
    //         setUsername(data.username);
    //         setEmail(data.email);
    //     }).catch((err) => {
    //         message.error(`Can not fetch user ${username}!`);
    //     })
    // }, []);

    const handleChangePassword = (e) => {
        changePassword({
            userId: userId,
            current_password: oldPassword,
            new_password: newPassword,
        }).then((data) => {
            message.success(`User password was changed successfully!`);
        }).catch((err) => {
            message.error(`User password failed to be changed!`);
        });
    };
    const handleDeleteAccount = (e) => {
        deleteAccount({
            userId: userId
        }).then((data) => {
            message.success(`User account was deleted successfully!`);
            localStorage.removeItem(LOGIN_TOKEN);
            navigateTo('/login');
        }).catch((err) => {
            message.error(`User account failed to be deleted!`);
        });
    }

    return (
        <div>
            <Card
                title={'User Profile'}
                style={{ width: 400, height: 280 }}
                actions={[
                    <Button type="primary" onClick={(e) => {
                        e.preventDefault();
                        setShowDeleteAccount(false);
                        setShowChangePassword(true);
                    }}>
                        Change Password
                    </Button>,
                    <Button type="danger" onClick={(e) => {
                        e.preventDefault();
                        setShowChangePassword(false);
                        setShowDeleteAccount(true);
                    }}>
                        Delete Account
                    </Button>,
                ]}
            >
                <p>
                    <strong>UserName:</strong> {username} <br/> <br/>
                    <strong>Email:</strong> {email}
                </p>
            </Card>
            <Modal
                title="Change Password"
                open={showChangePassword}
                onOk={handleChangePassword}
                onCancel={(e) => {
                    setShowChangePassword(false);
                    setNewPassword('');
                }}
                okText="Confirm"
                okType="danger"
            >
                <Input.Password
                    placeholder="Enter old password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                />
                <p></p>
                <Input.Password
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                />
            </Modal>
            <Modal
                title="Delete Account"
                open={showDeleteAccount}
                onOk={handleDeleteAccount}
                onCancel={(e)=> {
                    setShowDeleteAccount(false);
                }}
                okText="Delete"
                okType="danger"
            >
                <p>Are you sure to delete your account? This operation can not be reversed!</p>
            </Modal>
        </div>
    );
}

export default Profile;
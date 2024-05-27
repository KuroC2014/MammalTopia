import { useEffect, useState } from "react";
import { Button, Input, Space, Table, message } from "antd";
import { extractKeys, parseLoginToken } from "../utils/CommonUtils";
import { postEditFavor, postFavor } from "../requests/api";
import { LOGIN_TOKEN } from "../constants";

const mockData = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sydney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
];

function Favor() {

    const [favorList, setFavorList] = useState([]);
    const [columns, setColumns] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [dataCount, setDataCount] = useState(0);
    const [mammalName, setMammalName] = useState('');

    useEffect(() => {
        let loginTokenObj = parseLoginToken();
        postFavor({
            userId: loginTokenObj.userId,
            page: currentPage
        }).then((data) => {
            let favors = data.dataList;
            setDataCount(data.count);
            if (favors.length > 0) {
                const _columns = extractKeys(favors[0]);
                console.log("here: " + JSON.stringify(_columns));
                setColumns(_columns);
                setFavorList(favors);
            }
        }).catch((err) => {
            // let favors = mockData;
            // setDataCount(50);
            // if (favors.length > 0) {
            //     const _columns = extractKeys(favors[0]);
            //     console.log("here: " + JSON.stringify(_columns));
            //     setColumns(_columns);
            //     setFavorList(favors);
            // }
            message.error("Failed to query user's favorite list!")
        })
    }, [currentPage, mammalName]);

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const handleMammalNameChange = (e) => {
        setMammalName(e.target.value);
    };

    const handleEditFavor = (name, op) => {
        let loginTokenObj = parseLoginToken();
        postEditFavor({
            action: op,
            userId: loginTokenObj.userId,
            mammalName: name,
        }).then((data) => {
            message.success(`${op} mammal ${mammalName} successfully!`);
            setCurrentPage(1);
            setMammalName('')
        }).catch((err) => {
            message.error(`failed to ${op} mammal ${mammalName}!`);
        })
    }
    
    const handleAdd = (e) => {
        console.log("add " + mammalName);
        handleEditFavor(mammalName, 'add');
    };
    
    const handleRemove = (e) => {
        console.log("remove " + mammalName);
        handleEditFavor(mammalName, 'remove');
    };

    return (
        <Space direction="vertical" align="center" style={{ width: '100%' }}>
            <Space style={{ marginBottom: 16 }}>
                <Input
                    placeholder="Enter mammal's name"
                    value={mammalName}
                    onChange={handleMammalNameChange}
                    style={{ width: 200 }}
                />
                <Button type="primary" onClick={handleAdd}>
                    Add
                </Button>
                <Button type="danger" onClick={handleRemove}>
                    Remove
                </Button>
            </Space>
            <Table 
                dataSource={favorList} 
                columns={columns} 
                pagination={{
                    position: ['bottomRight'],
                    showSizeChanger: false,
                    current: currentPage,
                    total: dataCount,
                    pageSize: 10,
                    onChange: handlePageChange,
                }}
            />
        </Space>
    );
}

export default Favor;
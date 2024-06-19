<h1>Password Manager</h1>

This Password Manager is a simple Python script that securely manages your passwords. It uses the Fernet encryption scheme from the `cryptography` library to encrypt and decrypt passwords. The passwords are stored in a CSV file with specified fieldnames. The master password is stored in a binary file and is also encrypted using the Fernet encryption key.

<h2>Features</h2>

<ul>
    <li>Encrypt and decrypt passwords using Fernet encryption.</li>
    <li>Store and verify a master password.</li>
    <li>Create a new password manager file.</li>
    <li>Add new credentials to the password manager.</li>
    <li>View existing credentials.</li>
</ul>

<h2>Requirements</h2>

<ul>
    <li>Python 3.x</li>
    <li>
      cryptography library <br>
      &nbsp; Install cryptography library using pip: <br>
      &nbsp; pip install cryptography
    </li>
</ul>

<h2>Usage</h2>

<ol>
    <li><strong>Generate or Load Encryption Key:</strong> The script generates a new encryption key if the key file doesn't exist, or loads the existing key from the file. It ensures the key file has the appropriate permissions.</li>
    <li><strong>Store Master Password:</strong> Encrypt and store the master password in a binary file named <code>bin.txt</code>.</li>
    <li><strong>Verify Master Password:</strong> Verify if the master password entered by the user matches the master password stored in the binary file.</li>
    <li><strong>Create Password Manager File:</strong> Create a new password manager CSV file with specified fieldnames if it doesn't already exist.</li>
    <li><strong>Add New Credential:</strong> Add a new row to the password manager CSV file with the details of the new credential.</li>
    <li><strong>View Credential:</strong> View details of an existing password entry based on its title.</li>
</ol>

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>


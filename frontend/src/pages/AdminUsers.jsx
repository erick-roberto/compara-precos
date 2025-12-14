import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { userService } from "../api/users";
import { authService } from "../api/auth";
import "../css/AdminUsers.css";

function AdminUsers() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    user_type: "cliente"
  });
  const [successMessage, setSuccessMessage] = useState(null);

  // Verificar se é admin
  useEffect(() => {
    if (!authService.isAdmin()) {
      navigate("/");
    }
  }, [navigate]);

  // Carregar usuários
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log("Carregando usuários...");
      const data = await userService.getAllUsers();
      console.log("Usuários carregados:", data);
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Erro ao carregar usuários:", err);
      const errorMsg = err.response?.data?.error || err.message || "Erro ao carregar usuários";
      setError(errorMsg);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      
      // Validar dados
      if (!formData.name || formData.name.length < 2) {
        setError("Nome deve ter pelo menos 2 caracteres");
        return;
      }
      
      if (!formData.email || !formData.email.includes('@')) {
        setError("Email inválido");
        return;
      }
      
      if (!formData.password || formData.password.length < 6) {
        setError("Senha deve ter pelo menos 6 caracteres");
        return;
      }
      
      const userData = {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        user_type: formData.user_type
      };

      console.log("Criando usuário:", userData);
      await userService.createUser(userData);
      setSuccessMessage("Usuário criado com sucesso!");
      setFormData({ name: "", email: "", password: "", user_type: "cliente" });
      setShowForm(false);
      
      setTimeout(() => {
        setSuccessMessage(null);
        loadUsers();
      }, 2000);
    } catch (err) {
      console.error("Erro ao criar usuário:", err);
      const errorMsg = err.response?.data?.error || err.message || "Erro ao criar usuário";
      setError(errorMsg);
    }
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    try {
      setError(null);
      
      // Validar dados
      if (!formData.name || formData.name.length < 2) {
        setError("Nome deve ter pelo menos 2 caracteres");
        return;
      }
      
      const userData = {};
      if (formData.name) userData.name = formData.name;
      if (formData.user_type) userData.user_type = formData.user_type;

      console.log("Atualizando usuário:", editingUser.id, userData);
      await userService.updateUser(editingUser.id, userData);
      setSuccessMessage("Usuário atualizado com sucesso!");
      setFormData({ name: "", email: "", password: "", user_type: "cliente" });
      setEditingUser(null);
      setShowForm(false);
      
      setTimeout(() => {
        setSuccessMessage(null);
        loadUsers();
      }, 2000);
    } catch (err) {
      console.error("Erro ao atualizar usuário:", err);
      const errorMsg = err.response?.data?.error || err.message || "Erro ao atualizar usuário";
      setError(errorMsg);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm("Tem certeza que deseja deletar este usuário?")) {
      try {
        setError(null);
        console.log("Deletando usuário:", userId);
        await userService.deleteUser(userId);
        setSuccessMessage("Usuário deletado com sucesso!");
        
        setTimeout(() => {
          setSuccessMessage(null);
          loadUsers();
        }, 2000);
      } catch (err) {
        console.error("Erro ao deletar usuário:", err);
        const errorMsg = err.response?.data?.error || err.message || "Erro ao deletar usuário";
        setError(errorMsg);
      }
    }
  };

  const handleEditUser = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      email: user.email,
      password: "",
      user_type: user.user_type
    });
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingUser(null);
    setFormData({ name: "", email: "", password: "", user_type: "cliente" });
    setError(null);
  };

  return (
    <div className="admin-users-container">
      <div className="admin-header">
        <h1>Gerenciamento de Usuários</h1>
        <p>Administre todos os usuários do sistema</p>
      </div>

      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <div className="admin-controls">
        {!showForm && (
          <button 
            className="btn btn-primary"
            onClick={() => {
              setEditingUser(null);
              setFormData({ name: "", email: "", password: "", user_type: "cliente" });
              setShowForm(true);
            }}
          >
            + Novo Usuário
          </button>
        )}
      </div>

      {showForm && (
        <div className="user-form-container">
          <div className="user-form">
            <h2>{editingUser ? "Editar Usuário" : "Criar Novo Usuário"}</h2>
            
            <form onSubmit={editingUser ? handleUpdateUser : handleCreateUser}>
              <div className="form-group">
                <label htmlFor="name">Nome *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleFormChange}
                  placeholder="Nome completo"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleFormChange}
                  placeholder="email@example.com"
                  required={!editingUser}
                  disabled={editingUser ? true : false}
                />
              </div>

              {!editingUser && (
                <div className="form-group">
                  <label htmlFor="password">Senha *</label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleFormChange}
                    placeholder="Mínimo 6 caracteres"
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label htmlFor="user_type">Tipo de Usuário *</label>
                <select
                  id="user_type"
                  name="user_type"
                  value={formData.user_type}
                  onChange={handleFormChange}
                  required
                >
                  <option value="cliente">Cliente</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-success">
                  {editingUser ? "Atualizar" : "Criar"}
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={handleCancelForm}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading ? (
        <div className="loading">Carregando usuários...</div>
      ) : users.length === 0 ? (
        <div className="no-users">
          <p>Nenhum usuário encontrado</p>
          <p className="hint">Clique em "+ Novo Usuário" para criar o primeiro usuário</p>
        </div>
      ) : (
        <div className="users-table-container">
          <table className="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Email</th>
                <th>Tipo</th>
                <th>Data de Criação</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`badge badge-${user.user_type}`}>
                      {user.user_type === 'admin' ? 'Administrador' : 'Cliente'}
                    </span>
                  </td>
                  <td>{new Date(user.created_at).toLocaleDateString('pt-BR')}</td>
                  <td className="actions">
                    <button 
                      className="btn btn-small btn-edit"
                      onClick={() => handleEditUser(user)}
                    >
                      Editar
                    </button>
                    <button 
                      className="btn btn-small btn-delete"
                      onClick={() => handleDeleteUser(user.id)}
                    >
                      Deletar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default AdminUsers;

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GraphNeuralNetwork(nn.Module):
    """
    Graph Neural Network for analyzing propagation patterns and network anomalies in misinformation detection.
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        """
        Initializes the GNN architecture with two Graph Convolutional layers.

        Args:
            input_dim (int): Input feature dimension.
            hidden_dim (int): Hidden layer dimension.
            output_dim (int): Output classification dimension.
        """
        super(GraphNeuralNetwork, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, data: Data):
        """
        Forward pass of the GNN.

        Args:
            data (torch_geometric.data.Data): Graph data object.

        Returns:
            torch.Tensor: Log probabilities for classification.
        """
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)


if __name__ == "__main__":
    # Example synthetic graph data
    x = torch.tensor([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=torch.float)
    edge_index = torch.tensor([[0, 1, 2, 3], [1, 0, 3, 2]], dtype=torch.long)
    data = Data(x=x, edge_index=edge_index)

    model = GraphNeuralNetwork(input_dim=2, hidden_dim=4, output_dim=2)
    output = model(data)
    print(f"Graph Neural Network Output:\n{output}")

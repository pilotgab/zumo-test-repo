output "cluster_id" {
  description = "The EKS cluster ID"
  value       = aws_eks_cluster.zumo-eks.id
}

output "cluster_arn" {
  description = "The ARN of the EKS cluster"
  value       = aws_eks_cluster.zumo-eks.arn
}

output "cluster_endpoint" {
  description = "The endpoint for your EKS Kubernetes API"
  value       = aws_eks_cluster.zumo-eks.endpoint
}

output "cluster_certificate_authority_data" {
  description = "The certificate authority data for the EKS cluster"
  value       = aws_eks_cluster.zumo-eks.certificate_authority[0].data
}

output "node_group_id" {
  description = "The EKS node group ID"
  value       = aws_eks_node_group.zumo-eks-nodes.id
}

output "node_group_arn" {
  description = "The ARN of the EKS node group"
  value       = aws_eks_node_group.zumo-eks-nodes.arn
}

output "node_group_status" {
  description = "The status of the EKS node group"
  value       = aws_eks_node_group.zumo-eks-nodes.status
}

output "eks_role_arn" {
  description = "The ARN of the EKS role"
  value       = aws_iam_role.eks_role.arn
}

output "eks_node_role_arn" {
  description = "The ARN of the EKS node role"
  value       = aws_iam_role.eks_node_role.arn
}
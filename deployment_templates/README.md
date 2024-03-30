## Deployment files
- `deployment.yaml` -  Define how to run multiple instances of your application
- `service.yaml` - Tell your system how to find and connect to different running instances of your application
- `ingress.yaml` - Set up an entry point for users to access your application from outside the system

## How to create environment variables in secret

1. Prepare your environment variables in file `.env`

  Sample format:
  ```
  GOOGLE_API_KEY=your-google-api-key
  PINECONE_API_KEY=your-pinecone-api-key
  PINECONE_ENVIRONMENT=your-pinecone-env
  ```

2. Create the secret in kubernetes

  ```
  kubectl create secret generic bug-reporter-secret --from-env-file=.env
  ```
## How to build and deploy new docker image

1. Update version tag and build the image

  Example:
  ```
  docker buildx build --platform=linux/amd64 -t joyzoursky/ai-bug-report-generator:202403310000 .
  ```

2. Login to Docker and Push the image with new version tag

  Example:
  ```
  docker login
  docker push joyzoursky/ai-bug-report-generator:202403310000
  ```

3. Update the version in deployment.yaml and re-deploy the pod(s)

```
kubectl apply -f deployment.yaml
```

## How to debug when the site does not go up

Investigate with some logging commands
```
kubectl get pod
kubectl logs your-pod-name
kubectl describe pod your-pod-name

kubectl get deploy
kubectl describe deploy your-deploy-name

kubectl get service
kubectl describe service your-service-name

kubectl get ingress
kubectl describe ingress your-ingress-name
```
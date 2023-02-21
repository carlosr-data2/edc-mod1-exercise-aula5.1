resource "aws_lambda_function" "executa_emr" {
  # Cluster: EMR-Ney-IGTI-deltaTerminated with errorsThe subnet configuration was invalid: 
  # The subnet subnet-1df20360 does not exist.
  # 48 30
  filename      = "lambda_function_payload.zip" # este arquivo é criado na nossa esteira
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda.arn
  handler       = "lambda_function.handler"
  memory_size   = 128
  timeout       = 30

  source_code_hash = filebase64sha256("lambda_function_payload.zip") # faz o controle de estado

  runtime = "python3.8"

  tags = {
    IES   = "IGTI"
    CURSO = "EDC"
  }

}
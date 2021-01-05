
# def config(args):
#     print('S3 bucket configuration for uploading data')
#     data_s3 = s3_input()
#
#     if yes_with_question('Configure S3 bucket for adding images to readme? This bucket will need to be accessible from the git repo.'):
#         readme_s3 = s3_input()
#     else:
#         readme_s3 = None
#
#     new_config = config_tools.DefaultConfig(data_s3=data_s3, readme_s3=readme_s3)
#
#     new_config.save()
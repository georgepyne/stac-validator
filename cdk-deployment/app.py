#!/usr/bin/env python3

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
import aws_cdk as cdk
from validator_cdk.validator_cdk_stack import ValidatorCdkStack

app = cdk.App()
ValidatorCdkStack(app, "ValidatorCdkStack")
app.synth()

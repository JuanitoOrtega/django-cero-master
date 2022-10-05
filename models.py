# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActivityLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    log_name = models.CharField(max_length=191, blank=True, null=True)
    description = models.TextField()
    subject_type = models.CharField(max_length=191, blank=True, null=True)
    subject_id = models.PositiveBigIntegerField(blank=True, null=True)
    causer_type = models.CharField(max_length=191, blank=True, null=True)
    causer_id = models.PositiveBigIntegerField(blank=True, null=True)
    properties = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_log'


class AdjustmentProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    adjustment_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adjustment_products'


class Adjustments(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=191, blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adjustments'


class Antibiotics(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)
    shortcut = models.CharField(max_length=191, blank=True, null=True)
    commercial_name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'antibiotics'


class BranchProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    initial_quantity = models.FloatField()
    alert_quantity = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch_products'


class Branches(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    zoom_level = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    show_header_image = models.IntegerField()
    show_watermark_image = models.IntegerField()
    show_footer_image = models.IntegerField()
    header_image = models.CharField(max_length=191, blank=True, null=True)
    watermark_image = models.CharField(max_length=191, blank=True, null=True)
    footer_image = models.CharField(max_length=191, blank=True, null=True)
    report_footer = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branches'


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Chats(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_field = models.PositiveIntegerField(db_column='from', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to = models.PositiveIntegerField(blank=True, null=True)
    message = models.TextField()
    read = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chats'


class ContractPrices(models.Model):
    id = models.BigAutoField(primary_key=True)
    contract_id = models.IntegerField(blank=True, null=True)
    priceable_type = models.CharField(max_length=191, blank=True, null=True)
    priceable_id = models.PositiveBigIntegerField(blank=True, null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_prices'


class Contracts(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=191, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    discount_type = models.IntegerField(blank=True, null=True)
    discount_percentage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contracts'


class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    nationality = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class CultureComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    culture_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'culture_comments'


class CultureOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=191, blank=True, null=True)
    parent_id = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'culture_options'


class CulturePrices(models.Model):
    id = models.BigAutoField(primary_key=True)
    culture_id = models.IntegerField()
    branch_id = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'culture_prices'


class Cultures(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)
    sample_type = models.CharField(max_length=191, blank=True, null=True)
    precautions = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cultures'


class Currencies(models.Model):
    id = models.BigAutoField(primary_key=True)
    iso = models.CharField(max_length=191, blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    symbol = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'currencies'


class Doctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=191, blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    email = models.CharField(max_length=191, blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    commission = models.FloatField()

    class Meta:
        managed = False
        db_table = 'doctors'


class ExpenseCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expense_categories'


class Expenses(models.Model):
    id = models.BigAutoField(primary_key=True)
    expense_category_id = models.IntegerField(blank=True, null=True)
    payment_method_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField()
    date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    doctor_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class GroupCultureOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_culture_id = models.IntegerField(blank=True, null=True)
    culture_option_id = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_culture_options'


class GroupCultureResults(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_culture_id = models.IntegerField(blank=True, null=True)
    antibiotic_id = models.IntegerField(blank=True, null=True)
    sensitivity = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_culture_results'


class GroupCultures(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    culture_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    done = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    package_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_cultures'


class GroupPackages(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    package_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField()
    commission = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_packages'


class GroupPayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    payment_method_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField()
    date = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_payments'


class GroupTestResults(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_test_id = models.IntegerField(blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)
    result = models.CharField(max_length=191, blank=True, null=True)
    status = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_test_results'


class GroupTests(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField(blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    has_results = models.IntegerField()
    has_entered = models.IntegerField()
    done = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    package_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_tests'


class Groups(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.PositiveIntegerField(blank=True, null=True)
    patient_id = models.IntegerField(blank=True, null=True)
    doctor_id = models.IntegerField(blank=True, null=True)
    contract_id = models.IntegerField(blank=True, null=True)
    discount = models.FloatField()
    subtotal = models.FloatField()
    total = models.FloatField()
    paid = models.FloatField()
    due = models.FloatField()
    done = models.IntegerField()
    report_pdf = models.TextField(blank=True, null=True)
    receipt_pdf = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    barcode = models.CharField(max_length=191, blank=True, null=True)
    doctor_commission = models.FloatField()
    uploaded_report = models.IntegerField()
    sample_collection_date = models.CharField(max_length=191, blank=True, null=True)
    signed_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=191)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'jobs'


class Languages(models.Model):
    id = models.BigAutoField(primary_key=True)
    iso = models.CharField(max_length=191)
    active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    rtl = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'languages'


class Migrations(models.Model):
    migration = models.CharField(max_length=191)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Modules(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class OauthAccessTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    client_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=191, blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OauthAuthCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField()
    client_id = models.PositiveBigIntegerField()
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_auth_codes'


class OauthClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=191)
    secret = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=191, blank=True, null=True)
    redirect = models.TextField()
    personal_access_client = models.IntegerField()
    password_client = models.IntegerField()
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_clients'


class OauthPersonalAccessClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_personal_access_clients'


class OauthRefreshTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    access_token_id = models.CharField(max_length=100)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_refresh_tokens'


class PackagePrices(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_id = models.IntegerField()
    branch_id = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_prices'


class PackageTests(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_id = models.IntegerField(blank=True, null=True)
    testable_type = models.CharField(max_length=191)
    testable_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_tests'


class Packages(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    shortcut = models.CharField(max_length=191, blank=True, null=True)
    price = models.FloatField()
    precautions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'packages'


class PasswordResets(models.Model):
    email = models.CharField(max_length=191)
    token = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Patients(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=191, blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    gender = models.CharField(max_length=191, blank=True, null=True)
    dob = models.CharField(max_length=191, blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    email = models.CharField(max_length=191, blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    contract_id = models.IntegerField(blank=True, null=True)
    theme = models.CharField(max_length=191, blank=True, null=True)
    country_id = models.CharField(max_length=191, blank=True, null=True)
    national_id = models.CharField(max_length=191, blank=True, null=True)
    passport_no = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    last_activity = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients'


class PaymentMethods(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_methods'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    key = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'


class ProductConsumptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    testable_type = models.CharField(max_length=191, blank=True, null=True)
    testable_id = models.PositiveBigIntegerField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_consumptions'


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    sku = models.CharField(max_length=191, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class PurchasePayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    purchase_id = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=191, blank=True, null=True)
    payment_method_id = models.CharField(max_length=191, blank=True, null=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_payments'


class PurchaseProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    purchase_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField()
    quantity = models.FloatField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_products'


class Purchases(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=191, blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    subtotal = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    paid = models.FloatField()
    due = models.FloatField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchases'


class RolePermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role_id = models.IntegerField(blank=True, null=True)
    permission_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_permissions'


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=191, blank=True, null=True)
    value = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'


class Suppliers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    email = models.CharField(max_length=191, blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class TestComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_id = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_comments'


class TestConsumptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    testable_type = models.CharField(max_length=191, blank=True, null=True)
    testable_id = models.PositiveBigIntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_consumptions'


class TestOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_options'


class TestPrices(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_id = models.IntegerField()
    branch_id = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_prices'


class TestReferenceRanges(models.Model):
    id = models.BigAutoField(primary_key=True)
    test_id = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=191, blank=True, null=True)
    age_unit = models.CharField(max_length=191, blank=True, null=True)
    age_from = models.FloatField(blank=True, null=True)
    age_from_days = models.FloatField(blank=True, null=True)
    age_to = models.FloatField(blank=True, null=True)
    age_to_days = models.FloatField(blank=True, null=True)
    critical_low_from = models.CharField(max_length=191, blank=True, null=True)
    normal_from = models.CharField(max_length=191, blank=True, null=True)
    normal_to = models.CharField(max_length=191, blank=True, null=True)
    critical_high_from = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_reference_ranges'


class Tests(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=191, blank=True, null=True)
    shortcut = models.CharField(max_length=191, blank=True, null=True)
    sample_type = models.CharField(max_length=191, blank=True, null=True)
    unit = models.CharField(max_length=191, blank=True, null=True)
    reference_range = models.TextField(blank=True, null=True)
    type = models.TextField()
    separated = models.IntegerField()
    price = models.FloatField()
    status = models.IntegerField()
    title = models.IntegerField(blank=True, null=True)
    precautions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tests'


class Timezones(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timezones'


class TransferProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    transfer_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    from_branch_id = models.IntegerField(blank=True, null=True)
    to_branch_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transfer_products'


class Transfers(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=191, blank=True, null=True)
    from_branch_id = models.IntegerField(blank=True, null=True)
    to_branch_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transfers'


class UserBranches(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_branches'


class UserRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_roles'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191)
    email = models.CharField(unique=True, max_length=191)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=191)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    last_activity = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class VisitTests(models.Model):
    id = models.BigAutoField(primary_key=True)
    visit_id = models.IntegerField(blank=True, null=True)
    testable_type = models.CharField(max_length=191)
    testable_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visit_tests'


class Visits(models.Model):
    id = models.BigAutoField(primary_key=True)
    patient_id = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    zoom_level = models.IntegerField(blank=True, null=True)
    visit_date = models.CharField(max_length=191, blank=True, null=True)
    attach = models.CharField(max_length=191, blank=True, null=True)
    read = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    visit_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visits'
